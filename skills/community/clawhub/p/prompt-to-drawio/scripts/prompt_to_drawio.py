#!/usr/bin/env python3
"""CLI skill runtime for prompt-driven draw.io generation and editing."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib import error, request
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_VALIDATION_MODEL = DEFAULT_MODEL
SHAPE_LIBRARY_RAW_BASE = (
    "https://raw.githubusercontent.com/DayuanJiang/next-ai-draw-io/main/docs/shape-libraries"
)

AVAILABLE_SHAPE_LIBRARIES = [
    "alibaba_cloud",
    "android",
    "arrows2",
    "atlassian",
    "aws4",
    "azure2",
    "basic",
    "bpmn",
    "cabinets",
    "cisco19",
    "citrix",
    "electrical",
    "flowchart",
    "floorplan",
    "gcp2",
    "infographic",
    "kubernetes",
    "lean_mapping",
    "material_design",
    "mscae",
    "network",
    "openstack",
    "pid",
    "rack",
    "salesforce",
    "sap",
    "sitemap",
    "vvd",
    "webicons",
]

GENERIC_LIBRARY_HINTS: dict[str, str] = {
    "aws4": "Use style fragments like shape=mxgraph.aws4.resourceIcon; and resource names from AWS Architecture Icons.",
    "azure2": "Use style fragments like shape=mxgraph.azure2.resource; and Azure icon names.",
    "gcp2": "Use style fragments like shape=mxgraph.gcp2.resource; and GCP icon names.",
    "kubernetes": "Use style fragments like shape=mxgraph.kubernetes.<icon>; for pods/services/ingress/etc.",
    "flowchart": "Use standard draw.io flowchart styles such as rounded=1;rhombus;ellipse;endArrow=classic;.",
    "basic": "Use basic geometry styles: rectangle/ellipse/rhombus/hexagon with fillColor/strokeColor/rounded.",
}

GENERATION_SYSTEM_PROMPT = """You are an expert draw.io XML generator.
Return ONLY diagram XML content, without prose.
Preferred output is mxCell sibling elements (wrapper tags optional).
Rules:
1. Keep IDs unique.
2. Do not include id=0 or id=1 root cells when outputting raw mxCell.
3. Keep all mxCell elements siblings.
4. Escape XML special chars in attribute values.
5. Keep layout compact and readable.
"""

EDIT_SYSTEM_PROMPT = """You are an expert draw.io editor.
You receive current diagram XML and an edit request.
Output ONLY JSON object with this schema:
{
  "operations": [
    {
      "operation": "add|update|delete",
      "cell_id": "id",
      "new_xml": "<mxCell ...>...</mxCell>"  // required for add/update
    }
  ]
}
Rules:
1. Keep operation count minimal.
2. For add/update, new_xml must be a complete mxCell.
3. For update, new_xml id must equal cell_id.
4. For delete, omit new_xml.
5. Do not output markdown.
"""

VALIDATION_SYSTEM_PROMPT = """You are a diagram visual quality validator.
Return ONLY JSON with keys: valid (bool), issues (array), suggestions (array).
Issue item schema: {"type":"overlap|edge_routing|text|layout|rendering","severity":"critical|warning","description":"..."}
Set valid=true only when there are no critical issues.
"""


class SkillRuntimeError(Exception):
    """Raised for runtime failures."""


@dataclass
class ContextBundle:
    text_blocks: list[str]
    image_data_urls: list[str]


@dataclass
class DotenvBootstrapResult:
    enabled: bool
    source: Optional[Path]
    loaded_keys: int
    detail: str


DOTENV_BOOTSTRAP_RESULT = DotenvBootstrapResult(
    enabled=True,
    source=None,
    loaded_keys=0,
    detail="not-run",
)


class SimpleHTMLTextExtractor(HTMLParser):
    """Minimal HTML-to-text extractor for URL context."""

    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"} and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0:
            chunk = data.strip()
            if chunk:
                self._chunks.append(chunk)

    @property
    def text(self) -> str:
        return "\n".join(self._chunks)


def parse_dotenv_line(line: str) -> Optional[tuple[str, str]]:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    match = re.match(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", stripped)
    if not match:
        return None

    key = match.group(1)
    value = match.group(2).strip()

    if value and value[0] in {'"', "'"} and value[-1:] == value[0]:
        value = value[1:-1]
    else:
        if " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        elif value.startswith("#"):
            value = ""

    return key, value


def is_nonempty(value: Optional[str]) -> bool:
    return bool(value and value.strip())


def env_nonempty(*keys: str) -> Optional[str]:
    for key in keys:
        value = os.getenv(key)
        if is_nonempty(value):
            return value.strip()
    return None


def load_dotenv_file(path: Path) -> int:
    loaded = 0
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        raise SkillRuntimeError(f"Failed to read .env file {path}: {exc}") from exc

    for raw_line in content.splitlines():
        parsed = parse_dotenv_line(raw_line)
        if not parsed:
            continue
        key, value = parsed
        existing = os.getenv(key)
        if not is_nonempty(existing):
            os.environ[key] = value
            loaded += 1
    return loaded


def find_project_dotenv(explicit_file: Optional[str] = None) -> Optional[Path]:
    override = explicit_file or env_nonempty("DRAWIO_DOTENV_FILE")
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.exists():
            return candidate
        raise SkillRuntimeError(f"Dotenv file does not exist: {candidate}")

    cwd = Path.cwd().resolve()
    for folder in [cwd, *cwd.parents]:
        candidate = folder / ".env"
        if candidate.exists():
            return candidate
    return None


def parse_bootstrap_flags(argv: list[str]) -> tuple[bool, Optional[str]]:
    no_dotenv = False
    dotenv_file: Optional[str] = None

    idx = 0
    while idx < len(argv):
        token = argv[idx]
        if token == "--no-dotenv":
            no_dotenv = True
        elif token.startswith("--dotenv-file="):
            dotenv_file = token.split("=", 1)[1]
        elif token == "--dotenv-file" and idx + 1 < len(argv):
            dotenv_file = argv[idx + 1]
            idx += 1
        idx += 1
    return no_dotenv, dotenv_file


def bootstrap_project_env(no_dotenv: bool, dotenv_file: Optional[str]) -> DotenvBootstrapResult:
    if no_dotenv:
        return DotenvBootstrapResult(
            enabled=False,
            source=None,
            loaded_keys=0,
            detail="disabled (--no-dotenv)",
        )

    dotenv_path = find_project_dotenv(explicit_file=dotenv_file)
    if dotenv_path is None:
        return DotenvBootstrapResult(
            enabled=True,
            source=None,
            loaded_keys=0,
            detail="not-found",
        )

    loaded = load_dotenv_file(dotenv_path)
    return DotenvBootstrapResult(
        enabled=True,
        source=dotenv_path,
        loaded_keys=loaded,
        detail="loaded",
    )


def preprocess_argv(argv: list[str]) -> list[str]:
    subcommands = {"generate", "edit", "export", "validate", "library"}
    if not argv:
        return ["generate"]
    if argv[0] in {"-h", "--help"}:
        return argv
    if any(token in subcommands for token in argv):
        return argv
    return ["generate"] + argv


def parse_args() -> argparse.Namespace:
    argv = preprocess_argv(sys.argv[1:])
    no_dotenv, dotenv_file = parse_bootstrap_flags(argv)

    # Load .env before argparse defaults read os.environ.
    bootstrap = bootstrap_project_env(no_dotenv=no_dotenv, dotenv_file=dotenv_file)
    global DOTENV_BOOTSTRAP_RESULT
    DOTENV_BOOTSTRAP_RESULT = bootstrap

    parser = argparse.ArgumentParser(
        description="Prompt-driven draw.io generator/editor skill runtime.",
    )
    add_runtime_control_args(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_generate_parser(subparsers)
    add_edit_parser(subparsers)
    add_export_parser(subparsers)
    add_validate_parser(subparsers)
    add_library_parser(subparsers)

    args = parser.parse_args(argv)
    setattr(args, "_dotenv_bootstrap", bootstrap)
    return args


def add_common_prompt_args(parser: argparse.ArgumentParser) -> None:
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt", help="Natural-language prompt")
    source.add_argument("--prompt-file", help="Path to text file prompt")


def add_runtime_control_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--no-dotenv",
        action="store_true",
        help="Disable automatic .env loading.",
    )
    parser.add_argument(
        "--dotenv-file",
        help="Explicit .env file path (overrides auto-discovery).",
    )
    parser.add_argument(
        "--no-config-summary",
        action="store_true",
        help="Disable startup runtime configuration summary output.",
    )



def add_common_context_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        help="Attach local file as context (txt/md/pdf/json/csv/image)",
    )
    parser.add_argument(
        "--url",
        action="append",
        default=[],
        help="Attach URL page text as context",
    )
    parser.add_argument(
        "--shape-library",
        action="append",
        default=[],
        help="Attach draw.io shape library doc by name (repeatable)",
    )



def add_common_model_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model", default=env_nonempty("DRAWIO_LLM_MODEL") or DEFAULT_MODEL)
    parser.add_argument(
        "--base-url",
        default=env_nonempty("DRAWIO_LLM_BASE_URL") or DEFAULT_BASE_URL,
        help="OpenAI-compatible base URL",
    )
    parser.add_argument(
        "--api-key",
        default=env_nonempty("DRAWIO_LLM_API_KEY", "OPENAI_API_KEY"),
    )
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument(
        "--no-model-preflight",
        action="store_true",
        help="Skip provider model existence check before sending completion requests.",
    )



def add_common_render_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--out-image", help="Optional output image path")
    parser.add_argument(
        "--image-format",
        choices=["png", "svg", "pdf", "jpg"],
        help="Image format (auto-infer from --out-image suffix when omitted)",
    )
    parser.add_argument(
        "--no-docker-fallback",
        action="store_true",
        help="Disable Docker fallback for image rendering",
    )



def add_generate_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("generate", help="Generate a new .drawio diagram from prompt")
    add_runtime_control_args(parser)
    add_common_prompt_args(parser)
    add_common_context_args(parser)
    add_common_model_args(parser)
    add_common_render_args(parser)
    parser.add_argument("--out-drawio", required=True, help="Output .drawio path")
    parser.add_argument(
        "--minimal-style",
        action="store_true",
        help="Ask model to avoid decorative style and focus on structure",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run visual validation loop after generation",
    )
    parser.add_argument(
        "--validation-retries",
        type=int,
        default=2,
        help="Max retries when validation finds critical issues",
    )
    parser.add_argument(
        "--validation-model",
        default=env_nonempty("DRAWIO_VALIDATION_MODEL") or DEFAULT_VALIDATION_MODEL,
        help="Model for visual validation",
    )
    parser.add_argument(
        "--validate-soft",
        "--no-fail-on-validation",
        dest="validate_soft",
        action="store_true",
        help="When validation request/parse fails, keep generated files and exit with success.",
    )



def add_edit_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("edit", help="Edit an existing .drawio diagram from prompt")
    add_runtime_control_args(parser)
    add_common_prompt_args(parser)
    add_common_context_args(parser)
    add_common_model_args(parser)
    add_common_render_args(parser)
    parser.add_argument("--in-drawio", required=True, help="Existing .drawio path")
    parser.add_argument(
        "--out-drawio",
        help="Output .drawio path (default: overwrite input file)",
    )
    parser.add_argument(
        "--backup-dir",
        help="Backup directory (default: <drawio_dir>/.history)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run visual validation loop after editing",
    )
    parser.add_argument(
        "--validation-retries",
        type=int,
        default=2,
        help="Max retries when validation finds critical issues",
    )
    parser.add_argument(
        "--validation-model",
        default=env_nonempty("DRAWIO_VALIDATION_MODEL") or DEFAULT_VALIDATION_MODEL,
        help="Model for visual validation",
    )
    parser.add_argument(
        "--validate-soft",
        "--no-fail-on-validation",
        dest="validate_soft",
        action="store_true",
        help="When validation request/parse fails, keep edited files and exit with success.",
    )



def add_export_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("export", help="Export existing .drawio to image")
    add_runtime_control_args(parser)
    parser.add_argument("--in-drawio", required=True, help="Input .drawio file")
    parser.add_argument("--out-image", required=True, help="Output image path")
    parser.add_argument(
        "--image-format",
        choices=["png", "svg", "pdf", "jpg"],
        help="Image format (auto-infer from out-image suffix when omitted)",
    )
    parser.add_argument(
        "--no-docker-fallback",
        action="store_true",
        help="Disable Docker fallback for image rendering",
    )



def add_validate_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("validate", help="Run visual quality validation")
    add_runtime_control_args(parser)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--in-drawio", help="Input .drawio file")
    source.add_argument("--in-image", help="Input image file")
    parser.add_argument("--work-image", help="Temp image path when rendering from .drawio")
    parser.add_argument(
        "--validation-model",
        default=env_nonempty("DRAWIO_VALIDATION_MODEL") or DEFAULT_VALIDATION_MODEL,
    )
    parser.add_argument(
        "--validation-base-url",
        default=(
            env_nonempty("DRAWIO_VALIDATION_BASE_URL", "DRAWIO_LLM_BASE_URL")
            or DEFAULT_BASE_URL
        ),
    )
    parser.add_argument(
        "--validation-api-key",
        default=env_nonempty(
            "DRAWIO_VALIDATION_API_KEY",
            "DRAWIO_LLM_API_KEY",
            "OPENAI_API_KEY",
        ),
    )
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--fail-on-critical", action="store_true")
    parser.add_argument(
        "--no-model-preflight",
        action="store_true",
        help="Skip provider model existence check before validation requests.",
    )
    parser.add_argument(
        "--no-docker-fallback",
        action="store_true",
        help="Disable Docker fallback for image rendering",
    )



def add_library_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("library", help="List or fetch shape library docs")
    add_runtime_control_args(parser)
    parser.add_argument("--list", action="store_true", help="List available shape library names")
    parser.add_argument("--name", help="Shape library name")
    parser.add_argument("--out", help="Output markdown file path (default: print to stdout)")



def require_api_key(api_key: Optional[str]) -> str:
    if api_key and api_key.strip():
        return api_key.strip()
    raise SkillRuntimeError(
        "Missing API key for standalone CLI mode. "
        "Set DRAWIO_LLM_API_KEY (or OPENAI_API_KEY), provide --api-key, "
        "or place them in project .env."
    )



def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        text = args.prompt.strip()
    else:
        prompt_path = Path(args.prompt_file)
        if not prompt_path.exists():
            raise SkillRuntimeError(f"Prompt file not found: {prompt_path}")
        text = prompt_path.read_text(encoding="utf-8").strip()
    if not text:
        raise SkillRuntimeError("Prompt is empty.")
    return text



def normalize_base_url(base_url: str) -> str:
    cleaned = base_url.rstrip("/")
    if cleaned.endswith("/chat/completions"):
        return cleaned
    return f"{cleaned}/chat/completions"


def normalize_api_root(base_url: str) -> str:
    cleaned = base_url.rstrip("/")
    if cleaned.endswith("/chat/completions"):
        return cleaned[: -len("/chat/completions")]
    return cleaned


def mask_secret(value: Optional[str]) -> str:
    if not is_nonempty(value):
        return "EMPTY"
    return f"SET(len={len(value.strip())})"


def print_effective_config_summary(args: argparse.Namespace) -> None:
    if getattr(args, "no_config_summary", False):
        return

    bootstrap = getattr(args, "_dotenv_bootstrap", DOTENV_BOOTSTRAP_RESULT)
    print("[prompt-to-drawio] Runtime config:", file=sys.stderr)
    print(f"  command={args.command}", file=sys.stderr)

    dotenv_source = bootstrap.source if bootstrap.source else "None"
    print(
        "  dotenv="
        f"{bootstrap.detail}; source={dotenv_source}; loaded_keys={bootstrap.loaded_keys}",
        file=sys.stderr,
    )

    base_url = getattr(args, "base_url", None)
    model = getattr(args, "model", None)
    api_key = getattr(args, "api_key", None)
    validation_base_url = getattr(args, "validation_base_url", base_url)
    validation_model = getattr(args, "validation_model", None)
    validation_api_key = getattr(args, "validation_api_key", api_key)

    if base_url is not None:
        print(f"  base_url={base_url}", file=sys.stderr)
    if model is not None:
        print(f"  model={model}", file=sys.stderr)
    if hasattr(args, "api_key"):
        print(f"  api_key={mask_secret(api_key)}", file=sys.stderr)
    if validation_base_url is not None and (args.command in {"generate", "edit", "validate"}):
        print(f"  validation_base_url={validation_base_url}", file=sys.stderr)
    if validation_model is not None and (args.command in {"generate", "edit", "validate"}):
        print(f"  validation_model={validation_model}", file=sys.stderr)
    if args.command in {"generate", "edit", "validate"}:
        print(f"  validation_api_key={mask_secret(validation_api_key)}", file=sys.stderr)


def get_json(endpoint: str, headers: dict[str, str], timeout: int) -> dict[str, Any]:
    req = request.Request(endpoint, headers=headers, method="GET")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore") if exc.fp else ""
        raise SkillRuntimeError(
            f"HTTP {exc.code} from model endpoint: {endpoint}. {details[:500]}"
        ) from exc
    except error.URLError as exc:
        host = urlparse(endpoint).hostname or endpoint
        raise SkillRuntimeError(
            f"Network error calling model endpoint: {exc.reason}. "
            f"Check DNS/network access to {host}. "
            "If running in a restricted sandbox, rerun with network-enabled permissions."
        ) from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SkillRuntimeError(f"Model endpoint returned invalid JSON: {raw[:500]}") from exc


def normalize_model_id(value: str) -> str:
    cleaned = value.strip()
    if cleaned.startswith("models/"):
        return cleaned[len("models/") :]
    return cleaned


def extract_model_ids(payload: dict[str, Any]) -> set[str]:
    ids: set[str] = set()

    def maybe_add(value: Any) -> None:
        if isinstance(value, str) and value.strip():
            ids.add(normalize_model_id(value))

    data = payload.get("data")
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                maybe_add(item.get("id"))
                maybe_add(item.get("name"))
                maybe_add(item.get("model"))

    models = payload.get("models")
    if isinstance(models, list):
        for item in models:
            if isinstance(item, dict):
                maybe_add(item.get("id"))
                maybe_add(item.get("name"))
            else:
                maybe_add(item)

    for key in ("id", "name", "model"):
        maybe_add(payload.get(key))

    return ids


def list_available_models(api_key: str, base_url: str, timeout: int) -> tuple[Optional[set[str]], Optional[str]]:
    endpoint = f"{normalize_api_root(base_url)}/models"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        payload = get_json(endpoint, headers=headers, timeout=timeout)
    except SkillRuntimeError as exc:
        return None, str(exc)

    model_ids = extract_model_ids(payload)
    if not model_ids:
        return None, f"Model listing returned no ids from {endpoint}"
    return model_ids, None


def fallback_candidates_for_model(model: str) -> list[str]:
    requested = normalize_model_id(model)
    candidates: list[str] = []

    if requested == "gemini-3-pro":
        candidates.append("gemini-3-pro-preview")

    if requested.endswith("-pro") and not requested.endswith("-preview"):
        candidates.append(f"{requested}-preview")

    if requested.startswith("gemini-3"):
        candidates.extend(["gemini-3-pro-preview", "gemini-2.5-pro", "gemini-2.5-flash"])
    elif requested.startswith("gemini"):
        candidates.extend(["gemini-2.5-pro", "gemini-2.5-flash"])

    unique: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        normalized = normalize_model_id(item)
        if normalized not in seen:
            seen.add(normalized)
            unique.append(normalized)
    return unique


def preflight_model_choice(
    requested_model: str,
    api_key: str,
    base_url: str,
    timeout: int,
    no_model_preflight: bool,
    label: str,
) -> tuple[str, list[str]]:
    if no_model_preflight:
        return requested_model, []

    model_ids, error_text = list_available_models(api_key=api_key, base_url=base_url, timeout=timeout)
    if model_ids is None:
        return requested_model, [f"{label} preflight skipped: {error_text}"]

    requested = normalize_model_id(requested_model)
    if requested in model_ids:
        return requested, []

    for candidate in fallback_candidates_for_model(requested):
        if candidate in model_ids:
            return candidate, [f"{label} '{requested}' not found, fallback to '{candidate}'"]

    sample = ", ".join(sorted(model_ids)[:8])
    raise SkillRuntimeError(
        f"{label} '{requested}' not found on provider. "
        f"Available examples: {sample or 'N/A'}"
    )


def post_json(endpoint: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(endpoint, data=body, headers=headers, method="POST")

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="ignore") if exc.fp else ""
        raise SkillRuntimeError(f"HTTP {exc.code} from model endpoint: {details[:500]}") from exc
    except error.URLError as exc:
        host = urlparse(endpoint).hostname or endpoint
        raise SkillRuntimeError(
            f"Network error calling model endpoint: {exc.reason}. "
            f"Check DNS/network access to {host}. "
            "If running in a restricted sandbox, rerun with network-enabled permissions."
        ) from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SkillRuntimeError(f"Model endpoint returned invalid JSON: {raw[:500]}") from exc



def parse_message_content(message: dict[str, Any]) -> str:
    content = message.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        chunks: list[str] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") in {"text", "output_text"} and isinstance(item.get("text"), str):
                chunks.append(item["text"])
            elif isinstance(item.get("content"), str):
                chunks.append(item["content"])
        return "\n".join(chunks).strip()
    return ""



def call_chat_completion(
    messages: list[dict[str, Any]],
    model: str,
    api_key: str,
    base_url: str,
    temperature: float,
    max_tokens: int,
    timeout: int,
) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    endpoint = normalize_base_url(base_url)
    data = post_json(endpoint, payload, headers, timeout)
    choices = data.get("choices") or []
    if not choices:
        raise SkillRuntimeError("Model response did not contain choices.")

    message = choices[0].get("message") or {}
    text = parse_message_content(message)
    if not text:
        raise SkillRuntimeError("Model response message was empty.")
    return text



def strip_code_fences(text: str) -> str:
    matches = re.findall(r"```(?:json|xml)?\s*([\s\S]*?)```", text, flags=re.IGNORECASE)
    if matches:
        return max(matches, key=len).strip()
    return text.strip()


def iter_json_objects(text: str) -> list[str]:
    results: list[str] = []
    start: Optional[int] = None
    depth = 0
    in_string = False
    escaped = False

    for idx, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
                continue
            if ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue
        if ch == "{":
            if depth == 0:
                start = idx
            depth += 1
            continue
        if ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    results.append(text[start : idx + 1])
                    start = None

    return results


def auto_close_json_fragment(text: str) -> Optional[str]:
    in_string = False
    escaped = False
    depth = 0
    for ch in text:
        if in_string:
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
                continue
            if ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return None

    if depth <= 0:
        return text
    return f"{text}{'}' * depth}"


def dump_raw_response(prefix: str, raw: str) -> Path:
    fd, path_text = tempfile.mkstemp(prefix=f"{prefix}-", suffix=".txt")
    os.close(fd)
    path = Path(path_text)
    path.write_text(raw, encoding="utf-8", errors="ignore")
    return path


def parse_json_object_with_recovery(raw: str, context: str) -> dict[str, Any]:
    cleaned = strip_code_fences(raw)
    candidates: list[str] = []
    for item in [cleaned, raw]:
        item = item.strip()
        if item:
            candidates.append(item)

    object_candidates: list[str] = []
    for text in candidates:
        object_candidates.extend(iter_json_objects(text))
        first = text.find("{")
        if first != -1:
            closed = auto_close_json_fragment(text[first:])
            if closed:
                object_candidates.append(closed)

    merged: list[str] = []
    seen: set[str] = set()
    for item in candidates + sorted(object_candidates, key=len, reverse=True):
        if item not in seen:
            seen.add(item)
            merged.append(item)

    for candidate in merged:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed

    raw_path = dump_raw_response("drawio-json-parse", raw)
    raise SkillRuntimeError(
        f"{context} is not valid JSON after recovery. Raw response saved: {raw_path}"
    )



def extract_xml_segment(text: str) -> str:
    candidate = strip_code_fences(text)
    first = candidate.find("<")
    last = candidate.rfind(">")
    if first != -1 and last != -1 and first < last:
        return candidate[first : last + 1].strip()
    return candidate.strip()



def remove_root_cells(content: str) -> str:
    result = re.sub(
        r'<mxCell[^>]*\bid=["\']0["\'][^>]*(?:/?>.*?</mxCell>|/>)',
        "",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )
    result = re.sub(
        r'<mxCell[^>]*\bid=["\']1["\'][^>]*(?:/?>.*?</mxCell>|/>)',
        "",
        result,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return result.strip()



def repair_xml_entities(xml: str) -> str:
    return re.sub(
        r"&(?!(?:lt|gt|amp|quot|apos|#[0-9]+|#x[0-9a-fA-F]+);)",
        "&amp;",
        xml,
    )



def to_full_drawio_xml(model_output: str) -> str:
    xml = extract_xml_segment(model_output)
    if not xml:
        raise SkillRuntimeError("Model output is empty after XML extraction.")

    if "<mxfile" in xml:
        full = xml
    elif "<mxGraphModel" in xml:
        full = f'<mxfile><diagram name="Page-1" id="page-1">{xml}</diagram></mxfile>'
    else:
        if "<root>" in xml:
            xml = re.sub(r"</?root>", "", xml, flags=re.IGNORECASE).strip()
        xml = remove_root_cells(xml)
        full = (
            '<mxfile><diagram name="Page-1" id="page-1"><mxGraphModel><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            f"{xml}"
            "</root></mxGraphModel></diagram></mxfile>"
        )

    full = repair_xml_entities(full)
    try:
        ET.fromstring(full)
    except ET.ParseError as exc:
        raise SkillRuntimeError(f"Generated XML is invalid: {exc}") from exc
    return full



def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)



def read_drawio_xml(path: Path) -> str:
    if not path.exists():
        raise SkillRuntimeError(f"drawio file not found: {path}")
    xml = path.read_text(encoding="utf-8")
    if not xml.strip():
        raise SkillRuntimeError(f"drawio file is empty: {path}")
    try:
        ET.fromstring(xml)
    except ET.ParseError as exc:
        raise SkillRuntimeError(f"drawio file is invalid XML: {exc}") from exc
    return xml



def make_data_url_from_bytes(data: bytes, mime: str) -> str:
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{encoded}"



def guess_mime(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return "image/png"
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".gif":
        return "image/gif"
    if suffix == ".webp":
        return "image/webp"
    if suffix == ".svg":
        return "image/svg+xml"
    return "application/octet-stream"



def load_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        pdftotext = shutil.which("pdftotext")
        if not pdftotext:
            raise SkillRuntimeError(
                f"Cannot parse PDF {path}: install pypdf (pip) or pdftotext."
            )

        with tempfile.TemporaryDirectory(prefix="drawio-pdf-") as tmp:
            out = Path(tmp) / "out.txt"
            cmd = [pdftotext, str(path), str(out)]
            ok, err = run_command(cmd)
            if not ok:
                raise SkillRuntimeError(f"pdftotext failed for {path}: {err}")
            return out.read_text(encoding="utf-8", errors="ignore")

    reader = PdfReader(str(path))
    chunks: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            chunks.append(text.strip())
    return "\n\n".join(chunks)



def fetch_url_text(url: str, timeout: int = 30) -> str:
    req = request.Request(url, headers={"User-Agent": "drawio-skill/1.0"})
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            html = resp.read().decode(charset, errors="ignore")
    except Exception as exc:
        raise SkillRuntimeError(f"Failed to fetch URL {url}: {exc}") from exc

    parser = SimpleHTMLTextExtractor()
    parser.feed(html)
    text = parser.text.strip()
    if not text:
        raise SkillRuntimeError(f"URL had no extractable text: {url}")
    return text



def is_image_file(path: Path) -> bool:
    return path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}



def read_context_bundle(
    files: Iterable[str],
    urls: Iterable[str],
    shape_libraries: Iterable[str],
) -> ContextBundle:
    texts: list[str] = []
    images: list[str] = []

    for file_str in files:
        path = Path(file_str).expanduser().resolve()
        if not path.exists():
            raise SkillRuntimeError(f"Context file not found: {path}")

        if is_image_file(path):
            data = path.read_bytes()
            images.append(make_data_url_from_bytes(data, guess_mime(path)))
            continue

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            pdf_text = load_pdf_text(path)
            texts.append(f"[PDF: {path}]\n{pdf_text}")
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")
        texts.append(f"[FILE: {path}]\n{text}")

    for url in urls:
        page_text = fetch_url_text(url)
        texts.append(f"[URL: {url}]\n{page_text}")

    for lib in shape_libraries:
        lib_text = fetch_shape_library(lib)
        texts.append(f"[SHAPE_LIBRARY: {lib}]\n{lib_text}")

    return ContextBundle(text_blocks=texts, image_data_urls=images)



def compose_user_text(prompt: str, bundle: ContextBundle, extra_sections: Optional[list[str]] = None) -> str:
    chunks = [prompt]
    if extra_sections:
        chunks.extend(section for section in extra_sections if section)
    chunks.extend(bundle.text_blocks)
    return "\n\n".join(chunk for chunk in chunks if chunk.strip())



def build_user_content(prompt_text: str, image_data_urls: list[str]) -> str | list[dict[str, Any]]:
    if not image_data_urls:
        return prompt_text
    content: list[dict[str, Any]] = [{"type": "text", "text": prompt_text}]
    for data_url in image_data_urls:
        content.append({"type": "image_url", "image_url": {"url": data_url}})
    return content



def parse_operations_json(text: str) -> list[dict[str, Any]]:
    data = parse_json_object_with_recovery(text, context="Edit response")

    operations = data.get("operations")
    if not isinstance(operations, list):
        raise SkillRuntimeError("Edit response JSON missing operations array.")

    normalized: list[dict[str, Any]] = []
    for item in operations:
        if not isinstance(item, dict):
            continue
        op = item.get("operation")
        cell_id = item.get("cell_id")
        new_xml = item.get("new_xml")

        if op not in {"add", "update", "delete"}:
            continue
        if not isinstance(cell_id, str) or not cell_id.strip():
            continue
        rec: dict[str, Any] = {"operation": op, "cell_id": cell_id.strip()}
        if op in {"add", "update"}:
            if not isinstance(new_xml, str) or not new_xml.strip():
                raise SkillRuntimeError(f"Operation {op} requires new_xml for cell_id={cell_id}")
            rec["new_xml"] = extract_xml_segment(new_xml)
        normalized.append(rec)

    if not normalized:
        raise SkillRuntimeError("No valid operations parsed from edit response.")
    return normalized



def get_root_element(mxfile_root: ET.Element) -> ET.Element:
    mxgraph = mxfile_root.find(".//mxGraphModel")
    if mxgraph is None:
        raise SkillRuntimeError("drawio XML missing mxGraphModel")
    root = mxgraph.find("root")
    if root is None:
        root = ET.SubElement(mxgraph, "root")
    return root



def parse_cell_xml(cell_xml: str) -> ET.Element:
    try:
        cell = ET.fromstring(cell_xml)
    except ET.ParseError as exc:
        raise SkillRuntimeError(f"Invalid new_xml mxCell: {exc}") from exc
    if cell.tag != "mxCell":
        raise SkillRuntimeError("new_xml must have mxCell as root element")
    return cell



def build_cell_map(root: ET.Element) -> dict[str, ET.Element]:
    cell_map: dict[str, ET.Element] = {}
    for cell in root.findall("mxCell"):
        cid = cell.get("id")
        if cid:
            cell_map[cid] = cell
    return cell_map



def collect_descendants(root: ET.Element, start_ids: set[str]) -> set[str]:
    to_delete = set(start_ids)
    changed = True
    while changed:
        changed = False
        for cell in root.findall("mxCell"):
            cid = cell.get("id")
            parent = cell.get("parent")
            if cid and parent and parent in to_delete and cid not in to_delete:
                to_delete.add(cid)
                changed = True

        for cell in root.findall("mxCell"):
            cid = cell.get("id")
            source = cell.get("source")
            target = cell.get("target")
            if not cid:
                continue
            if (source in to_delete or target in to_delete) and cid not in to_delete:
                to_delete.add(cid)
                changed = True

    return to_delete



def apply_operations_to_drawio(drawio_xml: str, operations: list[dict[str, Any]]) -> str:
    mxfile = ET.fromstring(drawio_xml)
    root = get_root_element(mxfile)

    for op in operations:
        operation = op["operation"]
        cell_id = op["cell_id"]

        cell_map = build_cell_map(root)

        if operation == "update":
            existing = cell_map.get(cell_id)
            if existing is None:
                raise SkillRuntimeError(f"Update target cell not found: {cell_id}")
            new_cell = parse_cell_xml(op["new_xml"])
            new_cell_id = new_cell.get("id")
            if new_cell_id != cell_id:
                raise SkillRuntimeError(
                    f"Update ID mismatch: cell_id={cell_id}, new_xml.id={new_cell_id}"
                )

            children = list(root)
            idx = children.index(existing)
            root.remove(existing)
            root.insert(idx, new_cell)

        elif operation == "add":
            if cell_id in cell_map:
                raise SkillRuntimeError(f"Add target already exists: {cell_id}")
            new_cell = parse_cell_xml(op["new_xml"])
            new_cell_id = new_cell.get("id")
            if new_cell_id != cell_id:
                raise SkillRuntimeError(
                    f"Add ID mismatch: cell_id={cell_id}, new_xml.id={new_cell_id}"
                )
            root.append(new_cell)

        elif operation == "delete":
            if cell_id in {"0", "1"}:
                raise SkillRuntimeError("Cannot delete root cells 0 or 1")
            if cell_id not in cell_map:
                continue

            to_delete = collect_descendants(root, {cell_id})
            for cell in list(root):
                cid = cell.get("id")
                if cid in to_delete:
                    root.remove(cell)

    ensure_root_cells(mxfile)
    return ET.tostring(mxfile, encoding="unicode")



def ensure_root_cells(mxfile_root: ET.Element) -> None:
    root = get_root_element(mxfile_root)
    cell_map = build_cell_map(root)
    if "0" not in cell_map:
        root.insert(0, ET.Element("mxCell", {"id": "0"}))
        cell_map = build_cell_map(root)
    if "1" not in cell_map:
        root.insert(1, ET.Element("mxCell", {"id": "1", "parent": "0"}))



def run_command(cmd: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except OSError as exc:
        return False, str(exc)

    if completed.returncode == 0:
        return True, completed.stdout.strip()
    return False, (completed.stderr.strip() or completed.stdout.strip())



def resolve_image_format(image_path: Path, explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    suffix = image_path.suffix.lower().lstrip(".")
    if suffix in {"png", "svg", "pdf", "jpg"}:
        return suffix
    raise SkillRuntimeError(
        "Cannot infer image format from --out-image. Use --image-format png|svg|pdf|jpg"
    )



def render_with_cli(drawio_file: Path, image_file: Path, image_format: str) -> Optional[str]:
    candidates = [shutil.which("drawio"), shutil.which("draw.io")]
    candidates = [c for c in candidates if c]
    if not candidates:
        return None

    errors: list[str] = []
    for cli in candidates:
        commands = [
            [cli, "-x", "-f", image_format, "-o", str(image_file), str(drawio_file)],
            [
                cli,
                "--export",
                "--format",
                image_format,
                "--output",
                str(image_file),
                str(drawio_file),
            ],
        ]
        for cmd in commands:
            ok, info = run_command(cmd)
            if ok and image_file.exists():
                return ""
            if info:
                errors.append(f"{' '.join(cmd)} => {info}")

    return "\n".join(errors) if errors else "drawio CLI export failed"



def render_with_docker(drawio_file: Path, image_file: Path, image_format: str) -> Optional[str]:
    docker = shutil.which("docker")
    if not docker:
        return "Docker not found"

    in_dir = drawio_file.parent.resolve()
    out_dir = image_file.parent.resolve()
    cmd = [
        docker,
        "run",
        "--rm",
        "-v",
        f"{in_dir}:/in",
        "-v",
        f"{out_dir}:/out",
        "jgraph/drawio",
        "-x",
        "-f",
        image_format,
        "-o",
        f"/out/{image_file.name}",
        f"/in/{drawio_file.name}",
    ]

    ok, info = run_command(cmd)
    if ok and image_file.exists():
        return ""
    return info or "Docker drawio export failed"



def export_image(
    drawio_file: Path,
    out_image: Path,
    image_format: str,
    no_docker_fallback: bool,
) -> None:
    ensure_parent_dir(out_image)

    cli_error = render_with_cli(drawio_file, out_image, image_format)
    if out_image.exists():
        return

    if no_docker_fallback:
        detail = cli_error or "drawio CLI not found"
        raise SkillRuntimeError(f"Image export failed: {detail}")

    docker_error = render_with_docker(drawio_file, out_image, image_format)
    if out_image.exists():
        return

    raise SkillRuntimeError(
        "Image export failed.\n"
        f"CLI error: {cli_error or 'drawio CLI not found'}\n"
        f"Docker error: {docker_error}"
    )



def build_messages(system_prompt: str, user_text: str, image_data_urls: list[str]) -> list[dict[str, Any]]:
    content = build_user_content(user_text, image_data_urls)
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content},
    ]


def request_edit_operations(
    user_text: str,
    image_data_urls: list[str],
    model: str,
    api_key: str,
    base_url: str,
    temperature: float,
    max_tokens: int,
    timeout: int,
) -> list[dict[str, Any]]:
    messages = build_messages(EDIT_SYSTEM_PROMPT, user_text, image_data_urls)
    raw_ops = call_chat_completion(
        messages=messages,
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
    )
    try:
        return parse_operations_json(raw_ops)
    except SkillRuntimeError as first_exc:
        retry_user_text = (
            f"{user_text}\n\n"
            "Your previous output was invalid JSON or truncated. "
            "Return one complete JSON object only, no markdown fences."
        )
        retry_messages = build_messages(EDIT_SYSTEM_PROMPT, retry_user_text, image_data_urls)
        retry_raw = call_chat_completion(
            messages=retry_messages,
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        try:
            return parse_operations_json(retry_raw)
        except SkillRuntimeError as second_exc:
            raise SkillRuntimeError(
                "Edit response parse failed after retry. "
                f"First error: {first_exc}. "
                f"Second error: {second_exc}"
            ) from second_exc



def fetch_shape_library(name: str) -> str:
    normalized = name.strip().lower()
    if normalized not in AVAILABLE_SHAPE_LIBRARIES:
        raise SkillRuntimeError(
            f"Unknown shape library '{name}'. Use library --list to inspect supported names."
        )

    local_doc = (
        Path(__file__).resolve().parent.parent
        / "references"
        / "shape-libraries"
        / f"{normalized}.md"
    )
    if local_doc.exists():
        data = local_doc.read_text(encoding="utf-8", errors="ignore")
        if data.strip():
            return data

    fetch_errors: list[str] = []

    url = f"{SHAPE_LIBRARY_RAW_BASE}/{normalized}.md"
    req = request.Request(url, headers={"User-Agent": "drawio-skill/1.0"})
    try:
        with request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8", errors="ignore")
            if data.strip():
                return data
    except Exception as exc:
        fetch_errors.append(f"raw URL failed: {exc}")

    gh = shutil.which("gh")
    if gh:
        ok, output = run_command(
            [
                gh,
                "api",
                f"repos/DayuanJiang/next-ai-draw-io/contents/docs/shape-libraries/{normalized}.md",
                "--jq",
                ".content",
            ]
        )
        if ok and output.strip():
            try:
                decoded = base64.b64decode(output).decode("utf-8", errors="ignore")
                if decoded.strip():
                    return decoded
            except Exception as exc:
                fetch_errors.append(f"gh api decode failed: {exc}")
        elif output:
            fetch_errors.append(f"gh api failed: {output}")
    else:
        fetch_errors.append("gh CLI not found")

    generic_hint = GENERIC_LIBRARY_HINTS.get(
        normalized,
        "Use draw.io library-prefixed shape styles and verify icon keys by rendering test cells.",
    )
    return (
        f"# {normalized} (fallback)\n\n"
        f"Remote docs unavailable: {' | '.join(fetch_errors)}\n\n"
        f"{generic_hint}\n"
    )



def build_validation_payload_text(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)



def validate_image_via_llm(
    image_data_url: str,
    model: str,
    api_key: str,
    base_url: str,
    timeout: int,
) -> dict[str, Any]:
    messages = [
        {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Validate this diagram image."},
                {"type": "image_url", "image_url": {"url": image_data_url}},
            ],
        },
    ]

    raw = call_chat_completion(
        messages=messages,
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.0,
        max_tokens=2048,
        timeout=timeout,
    )

    try:
        parsed = parse_json_object_with_recovery(raw, context="Validation response")
    except SkillRuntimeError:
        retry_messages = [
            {"role": "system", "content": VALIDATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Return a complete valid JSON object only. "
                            "No markdown, no code fences."
                        ),
                    },
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                ],
            },
        ]
        retry_raw = call_chat_completion(
            messages=retry_messages,
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=0.0,
            max_tokens=2048,
            timeout=timeout,
        )
        parsed = parse_json_object_with_recovery(
            retry_raw,
            context="Validation response (retry)",
        )

    valid = bool(parsed.get("valid", False))
    issues = parsed.get("issues")
    suggestions = parsed.get("suggestions")

    if not isinstance(issues, list):
        issues = []
    if not isinstance(suggestions, list):
        suggestions = []

    return {
        "valid": valid,
        "issues": issues,
        "suggestions": suggestions,
    }



def write_backup(xml: str, source_path: Path, backup_dir: Optional[str]) -> Optional[Path]:
    if backup_dir:
        target_dir = Path(backup_dir).expanduser().resolve()
    else:
        target_dir = source_path.parent / ".history"

    target_dir.mkdir(parents=True, exist_ok=True)
    backup_name = f"{source_path.stem}-{int(time.time() * 1000)}.drawio"
    backup_path = target_dir / backup_name
    backup_path.write_text(xml, encoding="utf-8")
    return backup_path



def maybe_render(
    drawio_path: Path,
    out_image: Optional[str],
    image_format: Optional[str],
    no_docker_fallback: bool,
) -> Optional[Path]:
    if not out_image:
        return None
    image_path = Path(out_image).expanduser().resolve()
    fmt = resolve_image_format(image_path, image_format)
    export_image(drawio_path, image_path, fmt, no_docker_fallback)
    return image_path



def read_image_as_data_url(path: Path) -> str:
    data = path.read_bytes()
    return make_data_url_from_bytes(data, guess_mime(path))


def emit_warnings(items: Iterable[str]) -> None:
    for item in items:
        if item:
            print(f"WARNING: {item}", file=sys.stderr)



def generate_diagram(args: argparse.Namespace) -> int:
    api_key = require_api_key(args.api_key)
    generation_model, generation_notes = preflight_model_choice(
        requested_model=args.model,
        api_key=api_key,
        base_url=args.base_url,
        timeout=args.timeout,
        no_model_preflight=args.no_model_preflight,
        label="generation model",
    )
    validation_model = args.validation_model
    validation_notes: list[str] = []
    if args.validate:
        validation_model, validation_notes = preflight_model_choice(
            requested_model=args.validation_model,
            api_key=api_key,
            base_url=args.base_url,
            timeout=args.timeout,
            no_model_preflight=args.no_model_preflight,
            label="validation model",
        )
    emit_warnings([*generation_notes, *validation_notes])

    prompt = read_prompt(args)

    bundle = read_context_bundle(args.file, args.url, args.shape_library)

    style_note = "Use minimal black/white styling." if args.minimal_style else "Use professional readable styling."
    user_text = compose_user_text(prompt, bundle, extra_sections=[style_note])

    messages = build_messages(GENERATION_SYSTEM_PROMPT, user_text, bundle.image_data_urls)

    raw_xml = call_chat_completion(
        messages=messages,
        model=generation_model,
        api_key=api_key,
        base_url=args.base_url,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        timeout=args.timeout,
    )

    full_xml = to_full_drawio_xml(raw_xml)

    drawio_path = Path(args.out_drawio).expanduser().resolve()
    ensure_parent_dir(drawio_path)

    validation_result: Optional[dict[str, Any]] = None
    rendered_path: Optional[Path] = None
    validation_error: Optional[str] = None

    attempts = max(0, args.validation_retries) if args.validate else 0
    for attempt in range(attempts + 1):
        drawio_path.write_text(full_xml, encoding="utf-8")

        rendered_path = maybe_render(
            drawio_path=drawio_path,
            out_image=args.out_image,
            image_format=args.image_format,
            no_docker_fallback=args.no_docker_fallback,
        )

        if not args.validate:
            break

        validation_image: Path
        cleanup_temp = False
        if rendered_path and rendered_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
            validation_image = rendered_path
        else:
            with tempfile.NamedTemporaryFile(prefix="drawio-validate-", suffix=".png", delete=False) as tf:
                validation_image = Path(tf.name)
            cleanup_temp = True
            export_image(
                drawio_file=drawio_path,
                out_image=validation_image,
                image_format="png",
                no_docker_fallback=args.no_docker_fallback,
            )

        try:
            try:
                validation_result = validate_image_via_llm(
                    image_data_url=read_image_as_data_url(validation_image),
                    model=validation_model,
                    api_key=api_key,
                    base_url=args.base_url,
                    timeout=args.timeout,
                )
            except SkillRuntimeError as exc:
                validation_error = str(exc)
                break
        finally:
            if cleanup_temp and validation_image.exists():
                validation_image.unlink(missing_ok=True)

        if validation_error:
            break

        if validation_result.get("valid", False):
            break

        critical_issues = [
            issue
            for issue in validation_result.get("issues", [])
            if isinstance(issue, dict) and issue.get("severity") == "critical"
        ]
        if not critical_issues or attempt >= attempts:
            break

        feedback = (
            "Previous output failed visual validation. Regenerate diagram XML with fixes.\n"
            f"Validation report:\n{build_validation_payload_text(validation_result)}\n"
            "Previous XML:\n"
            f"{full_xml}"
        )
        retry_text = compose_user_text(prompt, bundle, extra_sections=[feedback, style_note])
        retry_messages = build_messages(
            GENERATION_SYSTEM_PROMPT,
            retry_text,
            bundle.image_data_urls,
        )
        retry_raw = call_chat_completion(
            messages=retry_messages,
            model=generation_model,
            api_key=api_key,
            base_url=args.base_url,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
        )
        full_xml = to_full_drawio_xml(retry_raw)

    drawio_path.write_text(full_xml, encoding="utf-8")
    print(f"DRAWIO_FILE={drawio_path}")
    if rendered_path and rendered_path.exists():
        print(f"IMAGE_FILE={rendered_path}")
    if validation_result is not None:
        print("VALIDATION_JSON=")
        print(build_validation_payload_text(validation_result))

    if validation_error:
        print(f"VALIDATION_ERROR={validation_error}", file=sys.stderr)
        if args.validate_soft:
            print("VALIDATION_STATUS=SOFT_FAILED", file=sys.stderr)
            return 0
        return 1

    return 0



def edit_diagram(args: argparse.Namespace) -> int:
    api_key = require_api_key(args.api_key)
    edit_model, edit_notes = preflight_model_choice(
        requested_model=args.model,
        api_key=api_key,
        base_url=args.base_url,
        timeout=args.timeout,
        no_model_preflight=args.no_model_preflight,
        label="edit model",
    )
    validation_model = args.validation_model
    validation_notes: list[str] = []
    if args.validate:
        validation_model, validation_notes = preflight_model_choice(
            requested_model=args.validation_model,
            api_key=api_key,
            base_url=args.base_url,
            timeout=args.timeout,
            no_model_preflight=args.no_model_preflight,
            label="validation model",
        )
    emit_warnings([*edit_notes, *validation_notes])

    prompt = read_prompt(args)

    in_path = Path(args.in_drawio).expanduser().resolve()
    out_path = Path(args.out_drawio).expanduser().resolve() if args.out_drawio else in_path

    current_xml = read_drawio_xml(in_path)
    backup_path = write_backup(current_xml, in_path, args.backup_dir)

    bundle = read_context_bundle(args.file, args.url, args.shape_library)

    user_text = compose_user_text(
        prompt,
        bundle,
        extra_sections=[
            "Current diagram XML (authoritative):",
            current_xml,
        ],
    )

    operations = request_edit_operations(
        user_text=user_text,
        image_data_urls=bundle.image_data_urls,
        model=edit_model,
        api_key=api_key,
        base_url=args.base_url,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        timeout=args.timeout,
    )
    edited_xml = apply_operations_to_drawio(current_xml, operations)

    ensure_parent_dir(out_path)

    validation_result: Optional[dict[str, Any]] = None
    rendered_path: Optional[Path] = None
    validation_error: Optional[str] = None

    attempts = max(0, args.validation_retries) if args.validate else 0
    for attempt in range(attempts + 1):
        out_path.write_text(edited_xml, encoding="utf-8")

        rendered_path = maybe_render(
            drawio_path=out_path,
            out_image=args.out_image,
            image_format=args.image_format,
            no_docker_fallback=args.no_docker_fallback,
        )

        if not args.validate:
            break

        with tempfile.NamedTemporaryFile(prefix="drawio-edit-validate-", suffix=".png", delete=False) as tf:
            validation_png = Path(tf.name)
        try:
            export_image(
                drawio_file=out_path,
                out_image=validation_png,
                image_format="png",
                no_docker_fallback=args.no_docker_fallback,
            )
            try:
                validation_result = validate_image_via_llm(
                    image_data_url=read_image_as_data_url(validation_png),
                    model=validation_model,
                    api_key=api_key,
                    base_url=args.base_url,
                    timeout=args.timeout,
                )
            except SkillRuntimeError as exc:
                validation_error = str(exc)
                break
        finally:
            validation_png.unlink(missing_ok=True)

        if validation_error:
            break

        if validation_result.get("valid", False):
            break

        critical_issues = [
            issue
            for issue in validation_result.get("issues", [])
            if isinstance(issue, dict) and issue.get("severity") == "critical"
        ]
        if not critical_issues or attempt >= attempts:
            break

        retry_prompt = (
            f"{prompt}\n\n"
            "Validation feedback:\n"
            f"{build_validation_payload_text(validation_result)}"
        )
        retry_text = compose_user_text(
            retry_prompt,
            bundle,
            extra_sections=["Current diagram XML (authoritative):", edited_xml],
        )
        retry_ops = request_edit_operations(
            user_text=retry_text,
            image_data_urls=bundle.image_data_urls,
            model=edit_model,
            api_key=api_key,
            base_url=args.base_url,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
        )
        edited_xml = apply_operations_to_drawio(edited_xml, retry_ops)

    out_path.write_text(edited_xml, encoding="utf-8")

    print(f"DRAWIO_FILE={out_path}")
    if backup_path:
        print(f"BACKUP_FILE={backup_path}")
    print(f"APPLIED_OPERATIONS={len(operations)}")
    if rendered_path and rendered_path.exists():
        print(f"IMAGE_FILE={rendered_path}")
    if validation_result is not None:
        print("VALIDATION_JSON=")
        print(build_validation_payload_text(validation_result))

    if validation_error:
        print(f"VALIDATION_ERROR={validation_error}", file=sys.stderr)
        if args.validate_soft:
            print("VALIDATION_STATUS=SOFT_FAILED", file=sys.stderr)
            return 0
        return 1

    return 0



def export_diagram(args: argparse.Namespace) -> int:
    drawio_path = Path(args.in_drawio).expanduser().resolve()
    read_drawio_xml(drawio_path)

    image_path = Path(args.out_image).expanduser().resolve()
    image_format = resolve_image_format(image_path, args.image_format)

    export_image(
        drawio_file=drawio_path,
        out_image=image_path,
        image_format=image_format,
        no_docker_fallback=args.no_docker_fallback,
    )

    print(f"DRAWIO_FILE={drawio_path}")
    print(f"IMAGE_FILE={image_path}")
    return 0



def validate_diagram(args: argparse.Namespace) -> int:
    api_key = require_api_key(args.validation_api_key)
    validation_model, notes = preflight_model_choice(
        requested_model=args.validation_model,
        api_key=api_key,
        base_url=args.validation_base_url,
        timeout=args.timeout,
        no_model_preflight=args.no_model_preflight,
        label="validation model",
    )
    emit_warnings(notes)

    if args.in_image:
        image_path = Path(args.in_image).expanduser().resolve()
        if not image_path.exists():
            raise SkillRuntimeError(f"Input image not found: {image_path}")
    else:
        drawio_path = Path(args.in_drawio).expanduser().resolve()
        read_drawio_xml(drawio_path)

        if args.work_image:
            image_path = Path(args.work_image).expanduser().resolve()
        else:
            fd, tmp_name = tempfile.mkstemp(prefix="drawio-validate-", suffix=".png")
            os.close(fd)
            image_path = Path(tmp_name)

        export_image(
            drawio_file=drawio_path,
            out_image=image_path,
            image_format="png",
            no_docker_fallback=args.no_docker_fallback,
        )

    result = validate_image_via_llm(
        image_data_url=read_image_as_data_url(image_path),
        model=validation_model,
        api_key=api_key,
        base_url=args.validation_base_url,
        timeout=args.timeout,
    )

    print(build_validation_payload_text(result))

    has_critical = any(
        isinstance(issue, dict) and issue.get("severity") == "critical"
        for issue in result.get("issues", [])
    )

    if args.fail_on_critical and has_critical:
        return 1
    return 0



def library_command(args: argparse.Namespace) -> int:
    if args.list:
        for name in AVAILABLE_SHAPE_LIBRARIES:
            print(name)
        return 0

    if not args.name:
        raise SkillRuntimeError("library command requires --name or --list")

    content = fetch_shape_library(args.name)
    if args.out:
        out = Path(args.out).expanduser().resolve()
        ensure_parent_dir(out)
        out.write_text(content, encoding="utf-8")
        print(f"LIBRARY_FILE={out}")
    else:
        print(content)
    return 0



def main() -> int:
    try:
        args = parse_args()
        print_effective_config_summary(args)
        if args.command == "generate":
            return generate_diagram(args)
        if args.command == "edit":
            return edit_diagram(args)
        if args.command == "export":
            return export_diagram(args)
        if args.command == "validate":
            return validate_diagram(args)
        if args.command == "library":
            return library_command(args)
        raise SkillRuntimeError(f"Unsupported command: {args.command}")
    except SkillRuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
