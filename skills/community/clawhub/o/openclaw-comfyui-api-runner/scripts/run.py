"""
Safe ComfyUI runner.

Supports:
- health check
- list built-in template workflows
- save/list/delete remembered server profiles
- submit generation from a built-in template, pasted JSON, uploaded JSON file, or stdin
- poll/watch for results and download every output image

All output is JSON. Run from skill root.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = SKILL_ROOT / "workflows"
GENERATED_DIR = SKILL_ROOT / "generated"
SEED_MAX = 2**32 - 1
DEFAULT_TIMEOUT_IMAGE = 120
DEFAULT_INTERVAL = 10

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comfy_client import (  # noqa: E402
    ComfyAPIError,
    delete_profile,
    fetch_url,
    get_base_url,
    get_history,
    health_check,
    list_profiles,
    post_prompt,
    resolve_config,
    save_profile,
    set_active_profile,
    set_default_server,
    set_default_workflow,
)
from parse_workflow import parse_workflow, parse_workflow_meta_only  # noqa: E402


def _apply_cli_env(args: argparse.Namespace) -> None:
    mapping = {
        "profile": "COMFYUI_PROFILE",
        "base_url": "COMFYUI_BASE_URL",
        "port": "COMFYUI_PORT",
        "api_key": "COMFYUI_API_KEY",
        "username": "COMFYUI_USERNAME",
        "password": "COMFYUI_PASSWORD",
    }
    for attr, env_name in mapping.items():
        value = getattr(args, attr, None)
        if value not in (None, ""):
            os.environ[env_name] = str(value)


def _list_workflows(workflows_dir: Path) -> list[dict[str, Any]]:
    if not workflows_dir.is_dir():
        return []
    result: list[dict[str, Any]] = []
    for path in sorted(workflows_dir.glob("*.json")):
        if path.name.endswith(".meta.json"):
            continue
        meta_path = path.with_name(path.stem + ".meta.json")
        try:
            if meta_path.is_file():
                varmap = parse_workflow_meta_only(meta_path)
            else:
                varmap = parse_workflow(path, None)
            result.append({
                "id": path.stem,
                "required": varmap.get("required", []),
                "optional": varmap.get("optional", []),
                "keywords": varmap.get("keywords", []),
            })
        except (OSError, json.JSONDecodeError, KeyError, FileNotFoundError):
            continue
    return result


def _apply_overrides(workflow: dict[str, Any], variables: dict[str, dict[str, str]], overrides: dict[str, Any]) -> None:
    for key, value in overrides.items():
        entry = variables.get(key)
        if not entry:
            continue
        node_id = entry.get("node")
        input_key = entry.get("input")
        if not node_id or node_id not in workflow:
            continue
        workflow.setdefault(node_id, {}).setdefault("inputs", {})[input_key] = value


def _randomize_literal_seeds(workflow: dict[str, Any]) -> None:
    """Randomize any literal seed inputs so repeat runs do not reuse the same seed."""
    for node in workflow.values():
        if not isinstance(node, dict):
            continue
        inputs = node.get("inputs")
        if not isinstance(inputs, dict):
            continue
        seed_value = inputs.get("seed")
        if isinstance(seed_value, list):
            continue
        if isinstance(seed_value, bool) or seed_value is None:
            continue
        if isinstance(seed_value, (int, float, str)):
            inputs["seed"] = random.randint(0, SEED_MAX)


def _load_template_workflow(template_id: str, skill_root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    workflow_path = skill_root / "workflows" / f"{template_id}.json"
    if not workflow_path.is_file():
        raise FileNotFoundError(f"Workflow not found: {workflow_path}")
    meta_path = workflow_path.with_suffix(".meta.json")
    varmap = parse_workflow(workflow_path, meta_path)
    with open(workflow_path, encoding="utf-8") as f:
        workflow = json.load(f)
    return workflow, varmap


def _find_workflow_by_keyword(query: str, skill_root: Path) -> str | None:
    needle = query.strip().lower()
    if not needle:
        return None
    matches: list[str] = []
    for path in sorted((skill_root / "workflows").glob("*.json")):
        if path.name.endswith(".meta.json"):
            continue
        meta_path = path.with_name(path.stem + ".meta.json")
        if not meta_path.is_file():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        keywords = [str(k).strip().lower() for k in (meta.get("keywords") or []) if str(k).strip()]
        if needle in keywords:
            matches.append(path.stem)
    if len(matches) == 1:
        return matches[0]
    return None


def _load_raw_workflow(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    if args.workflow_file:
        with open(Path(args.workflow_file), encoding="utf-8") as f:
            data = json.load(f)
        return data, f"file:{args.workflow_file}"
    if args.workflow_json:
        return json.loads(args.workflow_json), "json"
    if args.workflow_stdin:
        return json.loads(sys.stdin.read()), "stdin"
    raise FileNotFoundError("Missing workflow source. Use --workflow-file, --workflow-json, --workflow-stdin, or a template id.")


def _resolve_workflow(args: argparse.Namespace, skill_root: Path) -> tuple[dict[str, Any], str, dict[str, Any] | None]:
    """Return (workflow, source_label, varmap). varmap is only present for templates."""
    template_mode = bool((args.id or args.default_workflow) and not (args.workflow_file or args.workflow_json or args.workflow_stdin))
    if template_mode:
        template_id = args.id or args.default_workflow
        if not (skill_root / "workflows" / f"{template_id}.json").is_file():
            found = _find_workflow_by_keyword(template_id, skill_root)
            if found:
                template_id = found
        workflow, varmap = _load_template_workflow(template_id, skill_root)
        return workflow, f"template:{template_id}", varmap
    workflow, label = _load_raw_workflow(args)
    if not isinstance(workflow, dict):
        raise ValueError("Workflow JSON must be an object keyed by node id.")
    return workflow, label, None


def _extract_images(entry: dict[str, Any]) -> list[dict[str, Any]]:
    outputs = entry.get("outputs") or {}
    images: list[dict[str, Any]] = []
    for node_id, node_out in outputs.items():
        if not isinstance(node_out, dict):
            continue
        for idx, img in enumerate(node_out.get("images") or []):
            if not isinstance(img, dict) or not img.get("filename"):
                continue
            item = dict(img)
            item["node_id"] = str(node_id)
            item["image_index"] = idx
            images.append(item)
    return images


def _enrich_with_view_urls(history: dict[str, Any], base_url: str) -> dict[str, Any]:
    base = base_url.rstrip("/")
    for prompt_id, data in history.items():
        if not isinstance(data, dict):
            continue
        outputs = data.get("outputs") or {}
        for node_id, node_out in outputs.items():
            if not isinstance(node_out, dict):
                continue
            for img in node_out.get("images") or []:
                if not isinstance(img, dict) or "filename" not in img:
                    continue
                if img.get("view_url"):
                    continue
                fn = img["filename"]
                subfolder = img.get("subfolder", "")
                img_type = img.get("type", "output")
                q = f"filename={fn}&type={img_type}&subfolder={subfolder}"
                if prompt_id:
                    q += f"&prompt_id={prompt_id}"
                img["view_url"] = f"{base}/view?{q}"
    return history


def _safe_output_name(prompt_id: str, img: dict[str, Any]) -> str:
    original = Path(str(img.get("filename") or "image.png")).name
    stem = Path(original).stem or "image"
    suffix = Path(original).suffix or ".png"
    node_id = str(img.get("node_id") or "node")
    index = int(img.get("image_index") or 0)
    safe = f"{prompt_id}__{node_id}__{index}__{stem}{suffix}"
    return "".join(ch if ch.isalnum() or ch in {".", "-", "_"} else "_" for ch in safe)


def _download_outputs(prompt_id: str, entry: dict[str, Any], skill_root: Path) -> list[dict[str, Any]]:
    base_url = get_base_url(skill_root)
    wrapped = {prompt_id: entry}
    _enrich_with_view_urls(wrapped, base_url)
    enriched = wrapped[prompt_id]
    images = _extract_images(enriched)
    if not images:
        return []

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for img in images:
        view_url = img.get("view_url")
        if not view_url:
            continue
        local_name = _safe_output_name(prompt_id, img)
        local_path = GENERATED_DIR / local_name
        try:
            body = fetch_url(view_url, skill_root=skill_root)
            local_path.write_bytes(body)
        except Exception:
            continue
        results.append({
            "filename": img.get("filename"),
            "subfolder": img.get("subfolder", ""),
            "type": img.get("type", "output"),
            "view_url": view_url,
            "local_path": str(local_path.relative_to(skill_root)),
        })
    return results


def cmd_health(skill_root: Path) -> int:
    result = health_check(skill_root=skill_root)
    result["status"] = "health"
    print(json.dumps(result))
    return 0 if result.get("ok") else 1


def cmd_list(skill_root: Path) -> int:
    out = {
        "status": "workflows",
        "workflows": _list_workflows(skill_root / "workflows"),
    }
    print(json.dumps(out))
    return 0


def cmd_list_profiles() -> int:
    print(json.dumps({"status": "profiles", **list_profiles()}))
    return 0


def cmd_save_profile(args: argparse.Namespace) -> int:
    cfg = resolve_config()
    profile = {
        "base_url": cfg["base_url"],
        "port": cfg["port"],
    }
    if cfg.get("api_key"):
        profile["api_key"] = cfg["api_key"]
    if cfg.get("username"):
        profile["username"] = cfg["username"]
    if cfg.get("password"):
        profile["password"] = cfg["password"]
    out = save_profile(args.save_profile, profile, set_active=not args.no_activate)
    print(json.dumps({"status": "profiles", **out}))
    return 0


def cmd_delete_profile(args: argparse.Namespace) -> int:
    out = delete_profile(args.delete_profile)
    print(json.dumps({"status": "profiles", **out}))
    return 0


def cmd_set_active_profile(args: argparse.Namespace) -> int:
    out = set_active_profile(args.set_profile)
    print(json.dumps({"status": "profiles", **out}))
    return 0


def cmd_set_default_server(args: argparse.Namespace) -> int:
    out = set_default_server(args.set_default_server)
    print(json.dumps({"status": "profiles", **out}))
    return 0


def cmd_set_default_workflow(args: argparse.Namespace) -> int:
    out = set_default_workflow(args.set_default_workflow)
    print(json.dumps({"status": "profiles", **out}))
    return 0


def cmd_submit(args: argparse.Namespace, skill_root: Path) -> int:
    try:
        workflow, source, varmap = _resolve_workflow(args, skill_root)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(json.dumps({"status": "generation_submitted", "success": False, "error": str(e)}))
        return 1

    overrides: dict[str, Any] = {}
    if varmap is not None:
        if args.positive_prompt is not None:
            overrides["positive_prompt"] = args.positive_prompt
        if args.negative_prompt is not None:
            overrides["negative_prompt"] = args.negative_prompt
        if args.steps is not None:
            overrides["steps"] = args.steps
        if args.cfg is not None:
            overrides["cfg"] = args.cfg
        if args.sampler_name is not None:
            overrides["sampler_name"] = args.sampler_name
        if args.scheduler is not None:
            overrides["scheduler"] = args.scheduler
        if args.denoise is not None:
            overrides["denoise"] = args.denoise
        if getattr(args, "overrides", None):
            try:
                extra = json.loads(args.overrides)
                if isinstance(extra, dict):
                    overrides.update(extra)
            except json.JSONDecodeError:
                pass
        if "seed" in (varmap.get("variables") or {}):
            overrides["seed"] = random.randint(0, SEED_MAX)

        required = set(varmap.get("required") or [])
        missing = required - set(overrides.keys())
        if missing:
            print(json.dumps({"status": "generation_submitted", "success": False, "error": f"Missing required overrides: {sorted(missing)}"}))
            return 1
        _apply_overrides(workflow, varmap.get("variables") or {}, overrides)

    _randomize_literal_seeds(workflow)

    try:
        result = post_prompt(workflow, client_id=getattr(args, "client_id", None) or None, skill_root=skill_root)
    except ComfyAPIError as e:
        print(json.dumps({"status": "generation_submitted", "success": False, "error": e.body.get("message", str(e))}))
        return 1

    prompt_id = str(result.get("prompt_id") or "")
    out = {
        "status": "generation_submitted",
        "success": True,
        "prompt_id": prompt_id,
        "source": source,
        "watch_command": f"python3 scripts/run.py --watch {prompt_id}",
        "poll_command": f"python3 scripts/run.py --poll {prompt_id}",
        "message": "Run poll_command in a loop until done:true, or watch_command once and wait for exit.",
    }
    if args.serve_url:
        out["serve_hint"] = args.serve_url
    print(json.dumps(out))
    return 0


def _check_once_and_maybe_download(prompt_id: str, skill_root: Path) -> tuple[dict[str, Any], int]:
    try:
        result = get_history(prompt_id=prompt_id, skill_root=skill_root)
    except ComfyAPIError as e:
        return {
            "status": "generation_done",
            "done": False,
            "prompt_id": prompt_id,
            "error": e.body.get("message", str(e)),
        }, 1

    if not isinstance(result, dict):
        result = {}

    entry = result.get(prompt_id)
    if not isinstance(entry, dict) or not _extract_images(entry):
        return {
            "status": "generation_done",
            "done": False,
            "prompt_id": prompt_id,
            "message": "Still running. Run the same --poll command again in 10s.",
        }, 0

    outputs = _download_outputs(prompt_id, entry, skill_root)
    if not outputs:
        return {
            "status": "generation_done",
            "done": False,
            "prompt_id": prompt_id,
            "error": "No downloadable outputs found.",
        }, 1

    out = {
        "status": "generation_done",
        "done": True,
        "prompt_id": prompt_id,
        "outputs": outputs,
        "message": "Generation finished.",
    }
    out["view_url"] = outputs[0]["view_url"]
    out["local_path"] = outputs[0]["local_path"]
    return out, 0


def cmd_poll(args: argparse.Namespace, skill_root: Path) -> int:
    out, code = _check_once_and_maybe_download(args.prompt_id, skill_root)
    print(json.dumps(out))
    return code


def cmd_watch(args: argparse.Namespace, skill_root: Path) -> int:
    prompt_id = args.prompt_id
    timeout = args.timeout if args.timeout is not None else DEFAULT_TIMEOUT_IMAGE
    interval = max(1, args.interval)

    start = time.monotonic()
    while True:
        if time.monotonic() - start >= timeout:
            print(json.dumps({"status": "generation_done", "done": False, "prompt_id": prompt_id, "error": "Generation is taking longer than expected"}))
            return 1
        out, code = _check_once_and_maybe_download(prompt_id, skill_root)
        if out.get("done"):
            print(json.dumps(out))
            return 0
        if code != 0:
            print(json.dumps(out))
            return 1
        time.sleep(interval)


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe ComfyUI runner: profiles, raw workflows, health, submit, poll, watch.")
    parser.add_argument("--skill_root", type=Path, default=SKILL_ROOT, help="Skill root (default: auto)")
    parser.add_argument("--health", action="store_true", help="Check ComfyUI server health")
    parser.add_argument("--list", action="store_true", dest="list_workflows", help="List built-in template workflows")
    parser.add_argument("--list-profiles", action="store_true", help="List remembered server profiles")
    parser.add_argument("--save-profile", type=str, help="Save the current connection as a named profile")
    parser.add_argument("--delete-profile", type=str, help="Delete a saved profile")
    parser.add_argument("--set-profile", type=str, help="Mark a saved profile as active")
    parser.add_argument("--set-default-server", type=str, help="Set the default server to use")
    parser.add_argument("--set-default-workflow", type=str, help="Set the default workflow to use")
    parser.add_argument("--no-activate", action="store_true", help="Save profile without making it active")
    parser.add_argument("--gen", action="store_true", help="Submit a generation")
    parser.add_argument("--submit", action="store_true", help="Alias for --gen")
    parser.add_argument("--watch", action="store_true", help="Block until done or timeout (requires prompt_id); run in foreground.")
    parser.add_argument("--poll", action="store_true", help="Check once and return; run in a loop until done:true.")
    parser.add_argument("id", nargs="?", help="Template id for --gen, or prompt_id for --watch/--poll")
    parser.add_argument("--workflow-file", type=str, help="Path to a raw ComfyUI workflow JSON file")
    parser.add_argument("--workflow-json", type=str, help="Raw ComfyUI workflow JSON string")
    parser.add_argument("--workflow-stdin", action="store_true", help="Read raw workflow JSON from stdin")
    parser.add_argument("--positive_prompt", "--prompt", "-p", dest="positive_prompt", help="Positive prompt for template workflows")
    parser.add_argument("--negative_prompt", "-n", help="Negative prompt for template workflows")
    parser.add_argument("--steps", type=int, help="Steps override for template workflows")
    parser.add_argument("--cfg", type=float, help="CFG scale override for template workflows")
    parser.add_argument("--sampler_name", help="Sampler name override for template workflows")
    parser.add_argument("--scheduler", help="Scheduler override for template workflows")
    parser.add_argument("--denoise", type=float, help="Denoise override for template workflows")
    parser.add_argument("--client_id", help="Optional client_id UUID")
    parser.add_argument("--overrides", type=str, help="JSON object of extra overrides for template workflows")
    parser.add_argument("--timeout", type=int, default=None, help="Max wait seconds for --watch")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL, help="Poll interval for --watch (seconds)")
    parser.add_argument("--base-url", dest="base_url", help="ComfyUI base URL, e.g. http://127.0.0.1")
    parser.add_argument("--port", type=int, help="ComfyUI port, e.g. 8188")
    parser.add_argument("--api-key", dest="api_key", help="Optional ComfyUI API key")
    parser.add_argument("--username", help="Optional Basic-auth username")
    parser.add_argument("--password", help="Optional Basic-auth password")
    parser.add_argument("--profile", help="Use a remembered server profile for this run")
    parser.add_argument("--default-workflow", dest="default_workflow", help="Workflow to use when none is provided")
    parser.add_argument("--serve-url", help="Optional local viewer URL hint to echo back")

    args = parser.parse_args()
    _apply_cli_env(args)
    skill_root = args.skill_root
    if args.default_workflow is None:
        args.default_workflow = resolve_config(skill_root=skill_root).get("default_workflow")

    if args.health:
        return cmd_health(skill_root)
    if args.list_workflows:
        return cmd_list(skill_root)
    if args.list_profiles:
        return cmd_list_profiles()
    if args.save_profile:
        return cmd_save_profile(args)
    if args.delete_profile:
        return cmd_delete_profile(args)
    if args.set_profile:
        return cmd_set_active_profile(args)
    if args.set_default_server:
        return cmd_set_default_server(args)
    if args.set_default_workflow:
        return cmd_set_default_workflow(args)
    if args.gen or args.submit:
        return cmd_submit(args, skill_root)
    if args.watch:
        if not args.id:
            print(json.dumps({"status": "generation_done", "done": False, "error": "Missing prompt_id"}))
            return 1
        args.prompt_id = args.id
        return cmd_watch(args, skill_root)
    if args.poll:
        if not args.id:
            print(json.dumps({"status": "generation_done", "done": False, "error": "Missing prompt_id"}))
            return 1
        args.prompt_id = args.id
        return cmd_poll(args, skill_root)

    print(json.dumps({"status": "error", "error": "Use one of: --health, --list, --list-profiles, --save-profile, --delete-profile, --set-profile, --gen, --watch, --poll"}), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
