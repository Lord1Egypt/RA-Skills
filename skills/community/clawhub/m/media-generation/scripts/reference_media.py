#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Delegate image or video generation while handling reference-image transport.")
    p.add_argument("--mode", choices=["image", "video"], default="image", help="Target modality")
    p.add_argument("--prompt", required=True, help="Request prompt")
    p.add_argument("--reference-image", action="append", default=[], help="Repeatable reference image path")
    p.add_argument("--reference-key", default="reference_images", help="JSON field name used when passing encoded reference images to the provider in image mode only; video mode ignores this and uses multipart `input_reference`")
    p.add_argument("--transport", choices=["auto", "none", "provider-json"], default="auto", help="How to pass reference images; applies to image mode, while video mode always uses multipart `input_reference`")
    p.add_argument("--size", help="Forwarded size")
    p.add_argument("--quality", help="Forwarded image quality")
    p.add_argument("--style", help="Forwarded image style")
    p.add_argument("--background", help="Forwarded image background")
    p.add_argument("--n", type=int, help="Forwarded image count")
    p.add_argument("--seed", type=int, help="Forwarded seed")
    p.add_argument("--nsfw", choices=["true", "false"], help="Forwarded image NSFW flag")
    p.add_argument("--duration", help="Forwarded video duration")
    p.add_argument("--seconds", type=int, help="Forwarded video seconds")
    p.add_argument("--fps", type=int, help="Forwarded video fps")
    p.add_argument("--preset", choices=["normal", "fun", "spicy", "custom"], help="Forwarded video preset")
    p.add_argument("--provider", help="Forwarded provider name")
    p.add_argument("--config", help="Forwarded config path")
    p.add_argument("--model", help="Forwarded model name")
    p.add_argument("--endpoint", help="Forwarded endpoint path")
    p.add_argument("--status-endpoint-template", help="Forwarded video polling template")
    p.add_argument("--out-dir", help="Forwarded output directory")
    p.add_argument("--prefix", help="Forwarded output prefix")
    p.add_argument("--print-json", action="store_true", help="Print structured JSON summary")
    return p.parse_args()


def data_url_for(path: Path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def build_command(args, prompt, extra_json=None, extra_json_file=None):
    script_name = "generate_image.py" if args.mode == "image" else "generate_video.py"
    script_path = Path(__file__).resolve().parent / script_name
    cmd = [sys.executable, str(script_path), "--prompt", prompt]

    forwarded = {
        "--size": args.size,
        "--quality": args.quality if args.mode == "image" else None,
        "--style": args.style if args.mode == "image" else None,
        "--background": args.background if args.mode == "image" else None,
        "--n": args.n if args.mode == "image" else None,
        "--seed": args.seed,
        "--nsfw": args.nsfw if args.mode == "image" else None,
        "--duration": args.duration if args.mode == "video" else None,
        "--seconds": args.seconds if args.mode == "video" else None,
        "--fps": args.fps if args.mode == "video" else None,
        "--preset": args.preset if args.mode == "video" else None,
        "--provider": args.provider,
        "--config": args.config,
        "--model": args.model,
        "--endpoint": args.endpoint,
        "--status-endpoint-template": args.status_endpoint_template if args.mode == "video" else None,
        "--out-dir": args.out_dir,
        "--prefix": args.prefix,
    }
    for flag, value in forwarded.items():
        if value is not None:
            cmd.extend([flag, str(value)])
    if extra_json is not None:
        cmd.extend(["--extra-json", json.dumps(extra_json, ensure_ascii=False)])
    if extra_json_file is not None:
        cmd.extend(["--extra-json-file", str(extra_json_file)])
    if args.mode == "video" and args.reference_image:
        cmd.extend(["--input-reference", str(Path(args.reference_image[0]))])
    if args.print_json:
        cmd.append("--print-json")
    return cmd, script_name


def parse_output(text):
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except Exception:
        return stripped


def run_attempt(cmd, script_name, label):
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return {
        "label": label,
        "script": script_name,
        "command": cmd,
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
        "stdout": parse_output(proc.stdout),
        "stderr": proc.stderr.strip() or None,
        "stdoutRaw": proc.stdout,
    }


def main():
    args = parse_args()
    reference_paths = [Path(p) for p in args.reference_image]
    for path in reference_paths:
        if not path.exists():
            raise SystemExit(f"reference image not found: {path}")

    prompt = args.prompt.strip()
    summary = {
        "mode": args.mode,
        "referenceCount": len(reference_paths),
        "transport": args.transport,
        "prompt": prompt,
        "fallbackUsed": False,
        "result": None,
        "attempts": [],
        "hints": [
            "Image mode can use provider-json reference transport; video mode uses multipart `input_reference` instead.",
            "If image-mode provider-json transport fails, check whether the provider accepts encoded reference images and whether the reference key matches its schema.",
        ],
    }

    extra_json = None
    extra_json_file = None
    temp_path = None
    try:
        if args.mode == "image" and reference_paths and args.transport in {"auto", "provider-json"}:
            extra_json = {args.reference_key: [data_url_for(path) for path in reference_paths]}
            if len(json.dumps(extra_json, ensure_ascii=False)) > 50000:
                tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
                json.dump(extra_json, tmp, ensure_ascii=False)
                tmp.flush()
                tmp.close()
                temp_path = Path(tmp.name)
                extra_json_file = temp_path
                extra_json = None

        first_cmd, first_script = build_command(args, prompt, extra_json=extra_json, extra_json_file=extra_json_file)
        first = run_attempt(first_cmd, first_script, "primary")
        summary["attempts"].append({k: v for k, v in first.items() if k != "stdoutRaw"})
        if first["ok"]:
            summary["result"] = first["stdout"]
            if args.print_json:
                print(json.dumps(summary, ensure_ascii=False, indent=2))
            else:
                print(first["stdoutRaw"], end="")
            return

        if args.mode == "image" and reference_paths and args.transport == "auto":
            fallback_cmd, fallback_script = build_command(args, prompt, extra_json=None)
            fallback = run_attempt(fallback_cmd, fallback_script, "fallback-without-provider-json")
            summary["fallbackUsed"] = True
            summary["attempts"].append({k: v for k, v in fallback.items() if k != "stdoutRaw"})
            if fallback["ok"]:
                summary["result"] = fallback["stdout"]
                if args.print_json:
                    print(json.dumps(summary, ensure_ascii=False, indent=2))
                else:
                    print(fallback["stdoutRaw"], end="")
                return
            if args.print_json:
                print(json.dumps(summary, ensure_ascii=False, indent=2))
            else:
                if first["stderr"]:
                    print("INFO: provider-json reference transport failed; retrying without provider-json references", file=sys.stderr)
                if fallback["stderr"]:
                    print(fallback["stderr"], file=sys.stderr)
                if fallback["stdoutRaw"]:
                    print(fallback["stdoutRaw"], end="")
            raise SystemExit(fallback["returncode"])

        if args.print_json:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            if first["stderr"]:
                print(first["stderr"], file=sys.stderr)
            if first["stdoutRaw"]:
                print(first["stdoutRaw"], end="")
        raise SystemExit(first["returncode"])
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()


if __name__ == "__main__":
    main()
