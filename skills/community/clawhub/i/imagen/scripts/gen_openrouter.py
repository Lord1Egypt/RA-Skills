#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple


SUPPORTED_IMAGE_SIZES = {"1K", "2K", "4K"}
SUPPORTED_RATIOS = [
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
]


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_nested(obj: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    cur: Any = obj
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def resolve_openclaw_config() -> Path:
    env_path = os.environ.get("OPENCLAW_CONFIG")
    if env_path:
        path = Path(env_path).expanduser()
        if path.exists():
            return path

    default_path = Path("~/.openclaw/openclaw.json").expanduser()
    if default_path.exists():
        return default_path

    raise FileNotFoundError(
        "No se encontró openclaw.json. Define OPENCLAW_CONFIG o usa ~/.openclaw/openclaw.json"
    )


def resolve_default_agent_id(config: Dict[str, Any]) -> str:
    agents = get_nested(config, "agents", "list", default=[]) or []
    if isinstance(agents, list):
        for agent in agents:
            if isinstance(agent, dict) and agent.get("default") is True and agent.get("id"):
                return str(agent["id"])
        for agent in agents:
            if isinstance(agent, dict) and agent.get("id"):
                return str(agent["id"])
    return "main"


def resolve_auth_profiles_path(config: Dict[str, Any]) -> Path:
    env_path = os.environ.get("OPENCLAW_AUTH_PROFILES")
    if env_path:
        path = Path(env_path).expanduser()
        if path.exists():
            return path

    agent_id = resolve_default_agent_id(config)
    path = Path(f"~/.openclaw/agents/{agent_id}/agent/auth-profiles.json").expanduser()
    if path.exists():
        return path

    fallback = Path("~/.openclaw/agents/main/agent/auth-profiles.json").expanduser()
    if fallback.exists():
        return fallback

    raise FileNotFoundError(
        "No se encontró auth-profiles.json. Define OPENCLAW_AUTH_PROFILES o revisa tu instalación."
    )


def find_first_string_matching(obj: Any, pattern: re.Pattern[str]) -> Optional[str]:
    if isinstance(obj, str):
        return obj if pattern.search(obj) else None

    if isinstance(obj, dict):
        for value in obj.values():
            found = find_first_string_matching(value, pattern)
            if found:
                return found

    if isinstance(obj, list):
        for value in obj:
            found = find_first_string_matching(value, pattern)
            if found:
                return found

    return None


def resolve_openrouter_api_key(config: Dict[str, Any]) -> str:
    env_key = os.environ.get("OPENROUTER_API_KEY")
    if env_key:
        return env_key

    auth_path = resolve_auth_profiles_path(config)
    auth_data = load_json(auth_path)

    candidate_paths: Iterable[Tuple[str, ...]] = [
        ("profiles", "openrouter:default", "apiKey"),
        ("profiles", "openrouter:default", "api_key"),
        ("profiles", "openrouter:default", "token"),
        ("openrouter:default", "apiKey"),
        ("openrouter:default", "api_key"),
        ("openrouter:default", "token"),
    ]
    for path in candidate_paths:
        value = get_nested(auth_data, *path)
        if isinstance(value, str) and value.startswith("sk-or-"):
            return value

    found = find_first_string_matching(auth_data, re.compile(r"\bsk-or-[A-Za-z0-9_\-]+\b"))
    if found:
        return found

    raise RuntimeError(
        "No se encontró una API key válida de OpenRouter en OPENROUTER_API_KEY ni en auth-profiles.json"
    )


def resolve_image_models(config: Dict[str, Any]) -> Dict[str, str]:
    image_cfg = get_nested(config, "agents", "defaults", "imageModel", default={}) or {}
    primary = image_cfg.get("primary")
    fallbacks = image_cfg.get("fallbacks") or []

    if not primary:
        raise RuntimeError("agents.defaults.imageModel.primary no está configurado.")

    medium = fallbacks[0] if len(fallbacks) >= 1 else primary
    good = fallbacks[1] if len(fallbacks) >= 2 else medium
    top = fallbacks[2] if len(fallbacks) >= 3 else good

    return {
        "cheap": str(primary),
        "medium": str(medium),
        "good": str(good),
        "top": str(top),
    }


def normalize_openrouter_model_id(model_id: str) -> str:
    if model_id.startswith("openrouter/"):
        return model_id[len("openrouter/") :]
    return model_id


def detect_modalities(model_id: str) -> list[str]:
    m = model_id.lower()

    if (
        "gemini" in m
        or "gpt-5-image" in m
        or "gpt-image" in m
        or "nano-banana" in m
        or "seedream" in m
    ):
        return ["image", "text"]

    return ["image"]


def parse_ratio_string(value: str) -> Optional[Tuple[int, int]]:
    m = re.fullmatch(r"\s*(\d+)\s*:\s*(\d+)\s*", value)
    if not m:
        return None
    w = int(m.group(1))
    h = int(m.group(2))
    if w <= 0 or h <= 0:
        return None
    return (w, h)


def parse_exact_resolution(value: str) -> Optional[Tuple[int, int]]:
    m = re.fullmatch(r"\s*(\d{2,5})\s*[xX]\s*(\d{2,5})\s*", value)
    if not m:
        return None
    w = int(m.group(1))
    h = int(m.group(2))
    if w <= 0 or h <= 0:
        return None
    return (w, h)


def nearest_supported_ratio(width: int, height: int) -> str:
    target = width / height
    best_ratio = "1:1"
    best_delta = float("inf")

    for ratio in SUPPORTED_RATIOS:
        parsed = parse_ratio_string(ratio)
        if parsed is None:
            continue
        rw, rh = parsed
        delta = abs((rw / rh) - target)
        if delta < best_delta:
            best_delta = delta
            best_ratio = ratio

    return best_ratio


def infer_image_size_from_resolution(width: int, height: int) -> str:
    longest = max(width, height)
    area = width * height

    if longest <= 1400 and area <= 1_600_000:
        return "1K"
    if longest <= 2800 and area <= 6_000_000:
        return "2K"
    return "4K"


def resolve_size_and_ratio(
    size_arg: Optional[str],
    aspect_ratio_arg: Optional[str],
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Devuelve:
    - image_size normalizado: 1K/2K/4K o None
    - aspect_ratio normalizado o None
    - exact_resolution original si se pasó una resolución tipo 1920x1080
    """
    explicit_size = (size_arg or "").strip().upper()
    explicit_ratio = (aspect_ratio_arg or "").strip()
    exact_resolution_input: Optional[str] = None

    final_size: Optional[str] = None
    final_ratio: Optional[str] = None

    if explicit_size in SUPPORTED_IMAGE_SIZES:
        final_size = explicit_size

    if explicit_ratio in SUPPORTED_RATIOS:
        final_ratio = explicit_ratio

    parsed_resolution = parse_exact_resolution(explicit_size)
    if parsed_resolution:
        w, h = parsed_resolution
        exact_resolution_input = f"{w}x{h}"

        inferred_ratio = nearest_supported_ratio(w, h)
        inferred_size = infer_image_size_from_resolution(w, h)

        if explicit_size not in SUPPORTED_IMAGE_SIZES:
            final_size = inferred_size

        if explicit_ratio not in SUPPORTED_RATIOS:
            final_ratio = inferred_ratio

    parsed_ratio_resolution = parse_exact_resolution(explicit_ratio)
    if parsed_ratio_resolution:
        w, h = parsed_ratio_resolution
        exact_resolution_input = f"{w}x{h}"

        inferred_ratio = nearest_supported_ratio(w, h)
        inferred_size = infer_image_size_from_resolution(w, h)

        if explicit_ratio not in SUPPORTED_RATIOS:
            final_ratio = inferred_ratio

        if explicit_size not in SUPPORTED_IMAGE_SIZES and not parsed_resolution:
            final_size = inferred_size

    if explicit_ratio and explicit_ratio not in SUPPORTED_RATIOS:
        ratio_pair = parse_ratio_string(explicit_ratio)
        if ratio_pair:
            rw, rh = ratio_pair
            final_ratio = nearest_supported_ratio(rw, rh)

    return final_size, final_ratio, exact_resolution_input


def build_payload(model_id: str, prompt: str, size: Optional[str], aspect_ratio: Optional[str]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": model_id,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "modalities": detect_modalities(model_id),
        "stream": False,
    }

    image_config: Dict[str, Any] = {}
    if size:
        image_config["image_size"] = size
    if aspect_ratio:
        image_config["aspect_ratio"] = aspect_ratio

    if image_config:
        payload["image_config"] = image_config

    return payload


def openrouter_request(api_key: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    req = urllib.request.Request(
        url="https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openclaw.local",
            "X-Title": "OpenClaw imagen skill",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Error de red: {e}") from e


def extract_data_url(resp: Dict[str, Any]) -> str:
    choices = resp.get("choices") or []
    if not choices:
        raise RuntimeError("La respuesta no contiene choices.")

    message = choices[0].get("message") or {}

    images = message.get("images") or []
    for item in images:
        if isinstance(item, dict):
            if "image_url" in item and isinstance(item["image_url"], dict):
                url = item["image_url"].get("url")
                if isinstance(url, str) and url.startswith("data:image/"):
                    return url
            if "url" in item and isinstance(item["url"], str) and item["url"].startswith("data:image/"):
                return item["url"]
            if "data" in item and isinstance(item["data"], str) and item["data"].startswith("data:image/"):
                return item["data"]

    content = message.get("content")
    if isinstance(content, list):
        for part in content:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "image_url":
                image_url = part.get("image_url") or {}
                if isinstance(image_url, dict):
                    url = image_url.get("url")
                    if isinstance(url, str) and url.startswith("data:image/"):
                        return url

    raise RuntimeError("No se encontró ninguna imagen en la respuesta de OpenRouter.")


def decode_data_url(data_url: str) -> Tuple[bytes, str]:
    m = re.match(r"^data:(image/[\w.+-]+);base64,(.+)$", data_url, flags=re.DOTALL)
    if not m:
        raise RuntimeError("La imagen devuelta no tiene formato data URL base64 válido.")

    mime = m.group(1).strip().lower()
    b64 = m.group(2).strip()
    raw = base64.b64decode(b64)
    ext = mimetypes.guess_extension(mime) or ".png"
    if ext == ".jpe":
        ext = ".jpg"
    return raw, ext


def resolve_workspace_dir(custom_workspace_dir: Optional[str]) -> Path:
    candidates: list[Path] = []

    if custom_workspace_dir:
        candidates.append(Path(custom_workspace_dir).expanduser())

    env_workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if env_workspace:
        candidates.append(Path(env_workspace).expanduser())

    env_agent_workspace = os.environ.get("AGENT_WORKSPACE")
    if env_agent_workspace:
        candidates.append(Path(env_agent_workspace).expanduser())

    candidates.append(Path.cwd())

    for candidate in candidates:
        try:
            return candidate.resolve()
        except Exception:
            continue

    return Path.cwd().resolve()


def ensure_output_dir(custom_dir: Optional[str], workspace_dir: Path) -> Path:
    if custom_dir:
        custom_path = Path(custom_dir).expanduser()
        if custom_path.is_absolute():
            out_dir = custom_path.resolve()
        else:
            out_dir = (workspace_dir / custom_path).resolve()
    else:
        out_dir = (workspace_dir / "skills" / "imagen" / "out").resolve()

    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def save_image(data: bytes, ext: str, out_dir: Path, quality: str) -> Path:
    ts = time.strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"imagen-{quality}-{ts}{ext}"
    path.write_bytes(data)
    return path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Genera imágenes con OpenRouter usando la config de OpenClaw.")
    p.add_argument("--quality", choices=["cheap", "medium", "good", "top"], default="cheap")
    p.add_argument("--prompt", help="Prompt de la imagen.")
    p.add_argument(
        "--size",
        default=None,
        help="image_config.image_size (1K/2K/4K) o resolución exacta tipo 1920x1080. Si no se indica, no se envía.",
    )
    p.add_argument(
        "--aspect-ratio",
        default=None,
        help="image_config.aspect_ratio opcional (ej. 16:9). Si no se indica, no se envía.",
    )
    p.add_argument(
        "--workspace-dir",
        default=None,
        help="Workspace del agente. Si no se indica, usa OPENCLAW_WORKSPACE, AGENT_WORKSPACE o el cwd.",
    )
    p.add_argument(
        "--out-dir",
        default=None,
        help="Directorio de salida. Si es relativo, se resuelve dentro del workspace. "
             "Por defecto: skills/imagen/out",
    )
    p.add_argument("--timeout", type=int, default=300, help="Timeout HTTP en segundos.")
    p.add_argument("prompt_rest", nargs="*", help="Prompt alternativo posicional si no se usa --prompt")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    prompt = args.prompt.strip() if isinstance(args.prompt, str) and args.prompt.strip() else " ".join(args.prompt_rest).strip()
    if not prompt:
        eprint("ERROR: Falta el prompt.")
        return 2

    workspace_dir = resolve_workspace_dir(args.workspace_dir)

    config_path = resolve_openclaw_config()
    config = load_json(config_path)

    models = resolve_image_models(config)
    model_id = normalize_openrouter_model_id(models[args.quality])
    api_key = resolve_openrouter_api_key(config)

    resolved_size, resolved_ratio, exact_resolution_input = resolve_size_and_ratio(
        args.size,
        args.aspect_ratio,
    )

    payload = build_payload(
        model_id=model_id,
        prompt=prompt,
        size=resolved_size,
        aspect_ratio=resolved_ratio,
    )
    response = openrouter_request(api_key=api_key, payload=payload, timeout=args.timeout)
    data_url = extract_data_url(response)
    raw, ext = decode_data_url(data_url)

    out_dir = ensure_output_dir(args.out_dir, workspace_dir)
    out_file = save_image(raw, ext, out_dir, args.quality)

    result = {
        "ok": True,
        "quality": args.quality,
        "model": model_id,
        "config_path": str(config_path),
        "workspace_dir": str(workspace_dir),
        "output_dir": str(out_dir),
        "output_file": str(out_file),
        "image_size": resolved_size,
        "aspect_ratio": resolved_ratio,
        "requested_size": args.size,
        "requested_aspect_ratio": args.aspect_ratio,
        "exact_resolution_input": exact_resolution_input,
    }

    print(json.dumps(result, ensure_ascii=False))
    print(f"WORKSPACE_DIR={workspace_dir}")
    print(f"OUTPUT_DIR={out_dir}")
    print(f"OUTPUT_FILE={out_file}")
    print(f"QUALITY={args.quality}")
    print(f"MODEL={model_id}")
    if resolved_size:
        print(f"IMAGE_SIZE={resolved_size}")
    if resolved_ratio:
        print(f"ASPECT_RATIO={resolved_ratio}")
    if exact_resolution_input:
        print(f"EXACT_RESOLUTION_INPUT={exact_resolution_input}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        err = {"ok": False, "error": str(exc)}
        print(json.dumps(err, ensure_ascii=False))
        eprint(f"ERROR: {exc}")
        raise SystemExit(1)