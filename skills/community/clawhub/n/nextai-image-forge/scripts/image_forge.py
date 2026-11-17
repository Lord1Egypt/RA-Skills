#!/usr/bin/env python3
from __future__ import print_function

import argparse
import base64
import getpass
import html
import json
import os
import re
import secrets
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from mimetypes import guess_type
from urllib import error, parse, request


SKILL_VERSION = "0.1.0"
DEFAULT_MODEL = "gpt-image-2"
NEXTAI_API_ORIGIN = "https://www.nextai-code.com"
FIXED_API_URL = NEXTAI_API_ORIGIN + "/v1"
DEFAULT_SIZE = "1024x1024"
DEFAULT_OUTPUT_DIR = "."
VERSION_CHECK_UNAVAILABLE_MESSAGE = "Version check unavailable; continuing without update status."

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]+"),
    re.compile(r"(?i)((?:authorization\s*:\s*)?bearer\s+)([^\s,}]+)"),
    re.compile(r"(?i)((?:[\"']?api[_-]?key[\"']?|authorization|bearer|token|secret)\s*[:=]\s*)([\"']?)([^\"'\s,}]+)([\"']?)"),
]


class ImageForgeError(RuntimeError):
    def __init__(self, code, message):
        RuntimeError.__init__(self, message)
        self.code = code


def redact(text):
    result = str(text)
    for pattern in SECRET_PATTERNS:
        def replace(match):
            if len(match.groups()) >= 4:
                return match.group(1) + match.group(2) + "<REDACTED>" + match.group(4)
            if len(match.groups()) >= 2:
                return match.group(1) + "<REDACTED>"
            return "<REDACTED>"
        result = pattern.sub(replace, result)
    return result


def project_config_path(cwd):
    return os.path.join(cwd, ".image-forge", "config.json")


def user_secret_path(home):
    return os.path.join(home, ".config", "image-forge", "secrets.json")


def read_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as handle:
        return json.load(handle)


def write_json(path, data, mode=None):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent)
    if mode is not None:
        def opener(file_path, flags):
            fd = os.open(file_path, flags, mode)
            os.fchmod(fd, mode)
            return fd
        handle = open(path, "w", opener=opener)
    else:
        handle = open(path, "w")
    with handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")
    if mode is not None:
        os.chmod(path, mode)


def normalize_url(value):
    return (value or "").strip().rstrip("/")


def is_allowed_nextai_url(value):
    normalized = normalize_url(value)
    return normalized == NEXTAI_API_ORIGIN or normalized == FIXED_API_URL


def enforce_nextai_api_url(value):
    normalized = normalize_url(value)
    if normalized and not is_allowed_nextai_url(normalized):
        raise ImageForgeError(
            "invalid_api_url",
            "ImageForge NextAI edition only supports {0}/v1. Register and get an API key at {0}.".format(NEXTAI_API_ORIGIN),
        )
    return FIXED_API_URL


def configure_values(cwd, home, api_url=None, api_key=None, default_model=None):
    result = {"projectConfigSaved": False, "secretSaved": False}
    enforce_nextai_api_url(api_url)
    config_path = project_config_path(cwd)
    project_config = read_json(config_path)
    project_config["apiUrl"] = FIXED_API_URL
    if default_model:
        project_config["defaultModel"] = default_model
    if api_url is not None or default_model:
        write_json(config_path, project_config)
        result["projectConfigSaved"] = True
        result["projectConfigPath"] = config_path

    if api_key:
        secret_path = user_secret_path(home)
        secret_config = read_json(secret_path)
        secret_config["apiKey"] = api_key.strip()
        write_json(secret_path, secret_config, mode=0o600)
        result["secretSaved"] = True
        result["secretPath"] = secret_path
    return result


def load_effective_config(cwd=None, home=None, env=None):
    cwd = cwd or os.getcwd()
    home = home or os.path.expanduser("~")
    env = os.environ if env is None else env
    project_config = read_json(project_config_path(cwd))
    secret_config = read_json(user_secret_path(home))
    configured_api_url = env.get("IMAGE_FORGE_API_URL") or project_config.get("apiUrl") or FIXED_API_URL
    api_url = enforce_nextai_api_url(configured_api_url)
    api_key = env.get("IMAGE_FORGE_API_KEY") or secret_config.get("apiKey") or ""
    model = env.get("IMAGE_FORGE_MODEL") or project_config.get("defaultModel") or ""
    output_dir = project_config.get("outputDir") or DEFAULT_OUTPUT_DIR
    return {
        "apiUrl": api_url.rstrip("/"),
        "apiKey": api_key.strip(),
        "model": model,
        "outputDir": output_dir,
    }


def require_config(config):
    missing = []
    enforce_nextai_api_url(config.get("apiUrl"))
    if not config.get("apiKey"):
        missing.append("API key")
    if not config.get("model"):
        missing.append("model")
    if missing:
        raise ImageForgeError(
            "missing_config",
            "Missing {0}. Start ImageForge setup-server and complete the local setup page before continuing".format(
                ", ".join(missing),
            ),
        )
    return config


def api_endpoint(api_url, suffix):
    base = api_url.rstrip("/")
    if base.endswith("/v1"):
        return base + suffix
    return base + "/v1" + suffix


def build_generation_request(config, prompt, size=DEFAULT_SIZE, quality=None, n=1):
    require_config(config)
    payload = {"model": config["model"], "prompt": prompt, "size": size, "n": int(n)}
    if quality:
        payload["quality"] = quality
    body = json.dumps(payload).encode("utf-8")
    headers = {"Authorization": "Bearer " + config["apiKey"], "Content-Type": "application/json"}
    return api_endpoint(config["apiUrl"], "/images/generations"), headers, body


def guess_content_type(path):
    return guess_type(path)[0] or "application/octet-stream"


def multipart_body(fields, files, boundary):
    chunks = []
    for name, value in fields:
        chunks.append(("--" + boundary).encode("utf-8"))
        chunks.append(('Content-Disposition: form-data; name="{0}"'.format(name)).encode("utf-8"))
        chunks.append(b"")
        chunks.append(str(value).encode("utf-8"))
    for field_name, path in files:
        filename = os.path.basename(path)
        chunks.append(("--" + boundary).encode("utf-8"))
        chunks.append(('Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(field_name, filename)).encode("utf-8"))
        chunks.append(("Content-Type: " + guess_content_type(path)).encode("utf-8"))
        chunks.append(b"")
        with open(path, "rb") as handle:
            chunks.append(handle.read())
    chunks.append(("--" + boundary + "--").encode("utf-8"))
    chunks.append(b"")
    return b"\r\n".join(chunks)


def build_edit_request(config, image_paths, prompt, size=DEFAULT_SIZE):
    require_config(config)
    if not image_paths:
        raise ImageForgeError("missing_config", "Edit requires at least one --image path")
    for path in image_paths:
        if not os.path.exists(path):
            raise ImageForgeError("missing_config", "Image file not found: " + path)
    boundary = "imageforge-{0}".format(timestamp_slug())
    fields = [
        ("model", config["model"]),
        ("prompt", prompt),
        ("size", size),
    ]
    files = [("image", path) for path in image_paths]
    body = multipart_body(fields, files, boundary)
    headers = {
        "Authorization": "Bearer " + config["apiKey"],
        "Content-Type": "multipart/form-data; boundary=" + boundary,
    }
    return api_endpoint(config["apiUrl"], "/images/edits"), headers, body


def api_host(api_url):
    without_scheme = api_url.split("://", 1)[-1]
    return without_scheme.split("/", 1)[0]


def timestamp_slug():
    return datetime.utcnow().strftime("%Y%m%d-%H%M%S")


def safe_slug(value):
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "-", value.strip().lower()).strip("-")
    return cleaned[:48] or "image"


def resolve_default_output_dir(config, cwd=None):
    output_dir = config.get("outputDir") or DEFAULT_OUTPUT_DIR
    if os.path.isabs(output_dir):
        return output_dir
    return os.path.abspath(os.path.join(cwd or os.getcwd(), output_dir))


APPROVED_BRIEF_REQUIRED_FIELDS = (
    "Context",
    "Questions answered",
    "Approaches considered",
    "Selected direction",
    "Design confirmations",
    "Output",
    "Subject",
    "Style",
    "Composition",
    "Text",
    "Constraints",
    "Edit scope",
    "Brief self-review",
    "User approval",
)


def extract_approved_brief_fields(brief):
    field_pattern = re.compile(
        r"^({0}):\s*(.*)$".format("|".join(re.escape(field) for field in APPROVED_BRIEF_REQUIRED_FIELDS))
    )
    fields = {}
    current_field = None
    current_lines = []
    for raw_line in brief.splitlines():
        line = raw_line.strip()
        match = field_pattern.match(line)
        if match:
            if current_field:
                fields[current_field] = "\n".join(current_lines).strip()
            current_field = match.group(1)
            current_lines = []
            if match.group(2).strip():
                current_lines.append(match.group(2).strip())
        elif current_field:
            current_lines.append(line)
    if current_field:
        fields[current_field] = "\n".join(current_lines).strip()
    return fields


def validate_brief_fields_are_complete(fields):
    placeholder_pattern = re.compile(r"^(?:tbd|todo|placeholder|待定|未定|稍后补充|以后再说)$", re.I)
    incomplete = []
    for field in APPROVED_BRIEF_REQUIRED_FIELDS:
        value = fields.get(field, "").strip()
        if not value or placeholder_pattern.match(value):
            incomplete.append(field)
    if incomplete:
        raise ImageForgeError(
            "brief_required",
            "Approved Image Brief has empty or placeholder fields: {0}. Complete the Image Brief Brainstorming Workflow first.".format(", ".join(incomplete)),
        )


def validate_brief_has_brainstorming_evidence(fields):
    questions_answered = fields["Questions answered"]
    has_question = re.search(r"(^|\n)\s*(?:[-*]\s*)?(?:Q|问|问题)[:：]", questions_answered, re.I)
    has_answer = re.search(r"(^|\n)\s*(?:[-*]\s*)?(?:A|答|回答)[:：]", questions_answered, re.I)
    if not (has_question and has_answer):
        raise ImageForgeError(
            "brief_required",
            "Approved Image Brief must include question/answer evidence in Questions answered. Ask one clarifying question at a time before generating.",
        )

    approaches = fields["Approaches considered"]
    approach_markers = re.findall(
        r"(^|\n)\s*(?:[-*]\s*)?(?:Approach\s*)?(?:[ABC]|方案\s*[ABC])[:：]",
        approaches,
        re.I,
    )
    if len(approach_markers) < 2:
        raise ImageForgeError(
            "brief_required",
            "Approved Image Brief must include 2-3 approaches in Approaches considered before choosing a direction.",
        )

    confirmations = fields["Design confirmations"]
    if not re.search(r"confirmed|approved|确认|同意|通过", confirmations, re.I):
        raise ImageForgeError(
            "brief_required",
            "Approved Image Brief must include design confirmation evidence before generation or editing.",
        )

    approval = fields["User approval"].strip()
    if re.search(r"^(?:no|not approved|未确认|不同意|不通过)", approval, re.I) or not re.search(r"yes|approved|confirmed|确认|同意|通过", approval, re.I):
        raise ImageForgeError(
            "brief_required",
            "Approved Image Brief must include explicit User approval: yes/confirmed before generation or editing.",
        )


def validate_approved_brief(brief):
    missing = []
    if "Approved Image Brief" not in brief:
        missing.append("Approved Image Brief")
    fields = extract_approved_brief_fields(brief)
    missing.extend([field + ":" for field in APPROVED_BRIEF_REQUIRED_FIELDS if field not in fields])
    if missing:
        raise ImageForgeError(
            "brief_required",
            "A structured Approved Image Brief is required before generation or editing. Missing fields: {0}. Complete the Image Brief Brainstorming Workflow first, then rerun with --brief '<approved brief>'.".format(", ".join(missing)),
        )
    validate_brief_fields_are_complete(fields)
    validate_brief_has_brainstorming_evidence(fields)


def require_image_brief(brief=None, direct=False):
    if direct:
        return {
            "mode": "direct",
            "brief": "",
        }
    normalized_brief = (brief or "").strip()
    if normalized_brief:
        validate_approved_brief(normalized_brief)
        return {
            "mode": "brief",
            "brief": normalized_brief,
        }
    raise ImageForgeError(
        "brief_required",
        "Image Brief Gate required before generation or editing. Clarify the user's need, present an Approved Brief, wait for approval, then rerun with --brief '<approved brief>'. Use --direct only when the user explicitly asked to skip clarification.",
    )


def write_image_outputs(response, output_dir, output_name):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    written = []
    items = response.get("data") or []
    for index, item in enumerate(items, 1):
        name = "{0}-{1:02d}".format(output_name, index)
        image_path = os.path.join(output_dir, name + ".png")
        if item.get("b64_json"):
            image_bytes = base64.b64decode(item["b64_json"])
        else:
            raise ImageForgeError("protocol_error", "Image response did not include b64_json")
        with open(image_path, "wb") as handle:
            handle.write(image_bytes)
        written.append({"imagePath": image_path})
    if not written:
        raise ImageForgeError("protocol_error", "Image response did not include data")
    return written


def http_json(url, headers, body, timeout=120):
    req = request.Request(url, data=body, method="POST")
    for key, value in headers.items():
        req.add_header(key, value)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        if exc.code in (401, 403):
            raise ImageForgeError("auth_failed", "Authentication failed: " + redact(raw))
        raise ImageForgeError("provider_rejected", "Provider rejected request: " + redact(raw))
    except error.URLError as exc:
        raise ImageForgeError("network_error", "Network error: " + redact(exc))
    except ValueError:
        raise ImageForgeError("protocol_error", "Provider returned invalid JSON")


def generate_image(prompt, size=DEFAULT_SIZE, quality=None, n=1, output_dir=None, output_name=None, cwd=None, home=None, env=None, brief=None, direct=False):
    config = load_effective_config(cwd=cwd, home=home, env=env)
    url, headers, body = build_generation_request(config, prompt=prompt, size=size, quality=quality, n=n)
    require_image_brief(brief=brief, direct=direct)
    response = http_json(url, headers, body)
    final_output_dir = output_dir or resolve_default_output_dir(config, cwd=cwd)
    final_output_name = output_name or (timestamp_slug() + "-" + safe_slug(prompt))
    return write_image_outputs(response, final_output_dir, final_output_name)


def edit_image(image_paths, prompt, size=DEFAULT_SIZE, output_dir=None, output_name=None, cwd=None, home=None, env=None, brief=None, direct=False):
    image_paths = list(image_paths or [])
    config = load_effective_config(cwd=cwd, home=home, env=env)
    url, headers, body = build_edit_request(config, image_paths=image_paths, prompt=prompt, size=size)
    require_image_brief(brief=brief, direct=direct)
    try:
        response = http_json(url, headers, body)
    except ImageForgeError as exc:
        if len(image_paths) > 1 and exc.code in ("provider_rejected", "protocol_error"):
            raise ImageForgeError(
                "multi_image_unsupported",
                "Provider rejected multi-image editing. Retry with one --image. Details: " + redact(exc),
            )
        raise
    final_output_dir = output_dir or resolve_default_output_dir(config, cwd=cwd)
    final_output_name = output_name or (timestamp_slug() + "-" + safe_slug(prompt))
    return write_image_outputs(response, final_output_dir, final_output_name)


def doctor(cwd=None, home=None, env=None):
    cwd = cwd or os.getcwd()
    home = home or os.path.expanduser("~")
    config = load_effective_config(cwd=cwd, home=home, env=env)
    secret_path = user_secret_path(home)
    secret_mode = None
    if os.path.exists(secret_path):
        secret_mode = oct(os.stat(secret_path).st_mode & 0o777)
    return {
        "configured": bool(config.get("apiUrl") and config.get("apiKey") and config.get("model")),
        "apiHost": api_host(config["apiUrl"]) if config.get("apiUrl") else "",
        "model": config.get("model") or "",
        "apiKey": "configured" if config.get("apiKey") else "missing",
        "projectConfigPath": project_config_path(cwd),
        "userSecretPath": secret_path,
        "userSecretMode": secret_mode,
        "version": SKILL_VERSION,
    }


def preflight(cwd=None, home=None, env=None):
    cwd = cwd or os.getcwd()
    home = home or os.path.expanduser("~")
    config = load_effective_config(cwd=cwd, home=home, env=env)
    try:
        require_config(config)
    except ImageForgeError as exc:
        raise ImageForgeError(
            exc.code,
            str(exc) + ". Do not continue with image generation, editing, or local fallback until ImageForge is configured.",
        )
    return {
        "ready": True,
        "apiHost": api_host(config["apiUrl"]),
        "model": config["model"],
        "apiKey": "configured",
        "projectConfigPath": project_config_path(cwd),
        "userSecretPath": user_secret_path(home),
    }


def setup_interactive(cwd=None, home=None, input_func=None, secret_prompt_func=None):
    cwd = cwd or os.getcwd()
    home = home or os.path.expanduser("~")
    input_func = input_func or input
    secret_prompt_func = secret_prompt_func or getpass.getpass

    print("ImageForge uses NextAI Code API: {0}".format(FIXED_API_URL))
    print("Register and get an API key: {0}".format(NEXTAI_API_ORIGIN))
    model_answer = input_func("Default model [{0}]: ".format(DEFAULT_MODEL)).strip()
    default_model = model_answer or DEFAULT_MODEL
    api_key = secret_prompt_func("ImageForge API key: ")
    if api_key is not None:
        api_key = api_key.strip()

    configure_values(
        cwd=cwd,
        home=home,
        api_url=FIXED_API_URL,
        api_key=api_key,
        default_model=default_model,
    )
    return preflight(cwd=cwd, home=home, env={})


def setup_form_html(config, token, error_message=None):
    api_url = html.escape(FIXED_API_URL, quote=True)
    model = html.escape(config.get("model") or DEFAULT_MODEL, quote=True)
    escaped_token = html.escape(token, quote=True)
    escaped_error = html.escape(error_message or "")
    key_hint = (
        "已配置，留空则不修改。"
        if config.get("apiKey")
        else ""
    )
    api_key_required = "" if config.get("apiKey") else " required"
    api_key_placeholder = "留空则不修改" if config.get("apiKey") else "粘贴 NextAI Code API Key"
    error_block = ""
    if error_message:
        error_block = '<div class="alert alert-error" role="alert">{0}</div>'.format(escaped_error)
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>配置 ImageForge · NextAI Code</title>
  <style>
    :root {{
      --bg: #eef6ff;
      --panel: rgba(255,255,255,0.92);
      --panel-strong: #ffffff;
      --line: #d8e8fb;
      --text: #102033;
      --muted: #5f7390;
      --blue: #2563eb;
      --blue-2: #0ea5e9;
      --blue-soft: #dbeafe;
      --shadow: 0 24px 70px rgba(37, 99, 235, 0.14);
      --radius: 22px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background:
        radial-gradient(circle at 14% 12%, rgba(14,165,233,.22), transparent 28rem),
        radial-gradient(circle at 86% 4%, rgba(37,99,235,.18), transparent 24rem),
        linear-gradient(135deg, #f7fbff 0%, var(--bg) 52%, #e8f3ff 100%);
    }}
    .shell {{
      width: min(1120px, calc(100vw - 32px));
      min-height: min(720px, calc(100vh - 48px));
      margin: 24px auto;
      display: grid;
      grid-template-columns: 310px 1fr;
      overflow: hidden;
      border: 1px solid rgba(216,232,251,.9);
      border-radius: 28px;
      background: rgba(255,255,255,.68);
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }}
    aside {{
      padding: 30px;
      background: linear-gradient(180deg, rgba(219,234,254,.86), rgba(255,255,255,.68));
      border-right: 1px solid var(--line);
    }}
    .brand {{ display:flex; gap:12px; align-items:center; margin-bottom:34px; }}
    .logo {{
      width: 42px; height: 42px; border-radius: 14px;
      display:grid; place-items:center; color:white; font-weight:800;
      background: linear-gradient(135deg, var(--blue), var(--blue-2));
      box-shadow: 0 12px 28px rgba(37,99,235,.28);
    }}
    .brand b {{ display:block; font-size: 16px; }}
    .brand span {{ color: var(--muted); font-size: 12px; }}
    .steps {{ display:grid; gap:14px; }}
    .step {{
      display:grid; grid-template-columns: 32px 1fr; gap:12px; align-items:start;
      padding:14px; border-radius:16px; background:rgba(255,255,255,.58);
      border:1px solid rgba(216,232,251,.75);
    }}
    .num {{
      width:32px; height:32px; border-radius:11px; display:grid; place-items:center;
      background: var(--blue-soft); color: var(--blue); font-weight:800;
    }}
    .step strong {{ display:block; font-size:14px; }}
    .step small {{ color:var(--muted); line-height:1.45; }}
    main {{
      padding: 56px 64px;
      display:grid;
      align-content:center;
      background: linear-gradient(180deg, rgba(255,255,255,.9), rgba(248,251,255,.72));
    }}
    .card {{
      width: min(100%, 560px);
    }}
    .card {{ position: relative; }}
    .github-link {{
      position:absolute;
      top:0;
      right:0;
      width:40px;
      height:40px;
      display:grid;
      place-items:center;
      border-radius:13px;
      color:#1f2937;
      background:#f7fbff;
      border:1px solid #d7e7fb;
      text-decoration:none;
      transition: background .16s ease, transform .16s ease, border-color .16s ease;
    }}
    .github-link:hover {{ background:#fff; border-color:#b9d5f7; transform: translateY(-1px); }}
    .github-link svg {{ width:20px; height:20px; display:block; fill:currentColor; }}
    h1 {{
      margin:0 52px 30px;
      text-align:center;
      font-size: clamp(24px, 3vw, 32px);
      line-height:1.12;
      letter-spacing:-.035em;
    }}
    p {{ margin:0 0 24px; color:var(--muted); line-height:1.72; }}
    form {{ display:grid; gap:22px; }}
    .field {{ display:grid; gap:9px; }}
    .locked-url {{
      padding: 15px 16px;
      display:flex; justify-content:space-between; gap:16px; align-items:center;
      border-radius:16px;
      background: linear-gradient(180deg, #f8fbff, #f2f7ff);
      border:1px solid #d7e7fb;
    }}
    code {{ color:#0b4fb3; font-weight:750; word-break:break-all; }}
    .lock {{
      color:#2563eb;
      font-size:12px;
      font-weight:800;
      white-space:nowrap;
      padding:5px 9px;
      border-radius:999px;
      background:#eaf3ff;
      border:1px solid #c9ddff;
    }}
    label {{ display:block; margin:0; font-weight:800; font-size:14px; letter-spacing:-.01em; }}
    input {{
      width:100%; padding:14px 15px; border-radius:14px;
      border:1px solid #c7dcf5; background:rgba(255,255,255,.96); color:var(--text); font:inherit;
      outline:none; transition:border .18s ease, box-shadow .18s ease, background .18s ease;
    }}
    input:hover {{ background:#fff; }}
    input:focus {{ border-color:#60a5fa; box-shadow:0 0 0 4px rgba(96,165,250,.18); }}
    small {{ display:block; min-height: 18px; margin-top:7px; color:var(--muted); line-height:1.5; }}
    .input-row {{
      display:grid;
      grid-template-columns: 1fr auto;
      align-items: stretch;
    }}
    .input-row input {{
      border-radius:14px 0 0 14px;
      border-right: 0;
    }}
    .inline-link {{
      display:grid;
      place-items:center;
      padding:0 16px;
      border:1px solid #c7dcf5;
      border-radius:0 14px 14px 0;
      background:#eff6ff;
      color:var(--blue);
      font-weight:800;
      text-decoration:none;
      white-space:nowrap;
    }}
    .actions {{ display:flex; margin-top:4px; }}
    button {{
      width: 100%;
      border:0; border-radius:14px; padding:14px 18px; font-weight:850; cursor:pointer;
      font:inherit;
      background: #1769e8;
      color:white; box-shadow:0 14px 30px rgba(37,99,235,.22);
      transition: transform .16s ease, box-shadow .16s ease, background .16s ease;
    }}
    button:hover {{ background:#0f5fd6; box-shadow:0 18px 34px rgba(37,99,235,.28); }}
    button:active {{ transform: translateY(1px); }}
    .alert {{ margin: 0 0 18px; padding: 13px 15px; border-radius: 14px; line-height:1.55; }}
    .alert-error {{ background:#fff1f2; border:1px solid #fecdd3; color:#9f1239; }}
    @media (max-width: 820px) {{
      .shell {{ grid-template-columns: 1fr; }}
      aside {{ border-right:0; border-bottom:1px solid var(--line); }}
      main {{ padding: 28px 22px; }}
      .card {{ width: 100%; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <aside>
      <div class="brand"><div class="logo">N</div><div><b>NextAI Code</b><span>ImageForge Setup</span></div></div>
      <div class="steps">
        <div class="step"><div class="num">1</div><div><strong>注册 / 登录</strong></div></div>
        <div class="step"><div class="num">2</div><div><strong>获取 API Key</strong></div></div>
        <div class="step"><div class="num">3</div><div><strong>保存配置</strong></div></div>
      </div>
    </aside>
    <main>
      <section class="card">
        <a class="github-link" href="https://github.com/NextAI-Nova/nextai-skills" target="_blank" rel="noopener noreferrer" aria-label="GitHub repository">
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82A7.65 7.65 0 0 1 8 3.86c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8Z"></path></svg>
        </a>
        <h1>配置 ImageForge</h1>
        {error_block}
        <form method="post" action="/setup">
          <input type="hidden" name="token" value="{token}">
          <div class="field">
            <label>API URL</label>
            <div class="locked-url"><code>{api_url}</code><span class="lock">已锁定</span></div>
          </div>
          <div class="field">
            <label for="api_key">API Key</label>
            <div class="input-row">
              <input id="api_key" name="api_key" type="password" autocomplete="off" placeholder="{api_key_placeholder}"{api_key_required} autofocus>
              <a class="inline-link" href="{nextai_origin}" target="_blank" rel="noopener noreferrer">获取 API Key</a>
            </div>
            <small>{key_hint}</small>
          </div>
          <div class="field">
            <label for="default_model">默认模型</label>
            <input id="default_model" name="default_model" value="{model}" placeholder="{default_model}" required>
          </div>
          <div class="actions">
            <button type="submit">保存配置</button>
          </div>
        </form>
      </section>
    </main>
  </div>
</body>
</html>""".format(
        api_url=api_url,
        api_key_placeholder=html.escape(api_key_placeholder, quote=True),
        api_key_required=api_key_required,
        default_model=html.escape(DEFAULT_MODEL, quote=True),
        error_block=error_block,
        key_hint=html.escape(key_hint),
        model=model,
        nextai_origin=html.escape(NEXTAI_API_ORIGIN, quote=True),
        token=escaped_token,
    )


def setup_success_html(result):
    api_host_value = html.escape(result.get("apiHost") or "")
    model_value = html.escape(result.get("model") or "")
    return """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>配置已保存 · ImageForge</title>
  <style>
    body {{ margin:0; min-height:100vh; display:grid; place-items:center; font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; background:linear-gradient(135deg,#f7fbff,#e8f3ff); color:#102033; }}
    main {{ width:min(90vw,36rem); padding:34px; border-radius:24px; background:rgba(255,255,255,.92); border:1px solid #d8e8fb; box-shadow:0 24px 70px rgba(37,99,235,.14); }}
    .badge {{ display:inline-block; padding:7px 11px; border-radius:999px; background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe; font-weight:800; font-size:13px; }}
    h1 {{ margin:18px 0 12px; font-size:32px; letter-spacing:-.03em; }}
    p {{ color:#5f7390; line-height:1.65; }}
    code {{ color:#0f4fb7; font-weight:800; }}
  </style>
</head>
<body>
  <main>
    <span class="badge">NextAI Code 已连接</span>
    <h1>配置已保存</h1>
    <p>接口地址：<code>{api_host}</code></p>
    <p>模型：<code>{model}</code></p>
    <p>可以关闭这个页面，回到 Agent 继续生成或编辑图片。</p>
  </main>
</body>
</html>""".format(api_host=api_host_value, model=model_value)


def create_setup_server(cwd=None, home=None, host="127.0.0.1", port=0, token=None):
    cwd = cwd or os.getcwd()
    home = home or os.path.expanduser("~")
    token = token or secrets.token_urlsafe(32)
    state = {"completed": False, "result": None, "token": token}

    class SetupHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            return

        def send_html(self, status, body):
            encoded = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def token_from_query(self):
            parsed = parse.urlparse(self.path)
            return (parse.parse_qs(parsed.query).get("token") or [""])[0]

        def authorized(self, fields=None):
            candidates = [self.token_from_query()]
            if fields:
                candidates.extend(fields.get("token") or [])
            return token in candidates

        def do_GET(self):
            parsed = parse.urlparse(self.path)
            if parsed.path not in ("/", "/setup"):
                self.send_html(404, "Not found")
                return
            if not self.authorized():
                self.send_html(403, "Invalid or expired setup link")
                return
            config = load_effective_config(cwd=cwd, home=home, env={})
            self.send_html(200, setup_form_html(config=config, token=token))

        def do_POST(self):
            parsed = parse.urlparse(self.path)
            if parsed.path != "/setup":
                self.send_html(404, "Not found")
                return
            length = int(self.headers.get("Content-Length") or "0")
            if length > 65536:
                self.send_html(413, "Request too large")
                return
            raw_body = self.rfile.read(length).decode("utf-8")
            fields = parse.parse_qs(raw_body, keep_blank_values=True)
            if not self.authorized(fields):
                self.send_html(403, "Invalid or expired setup link")
                return

            existing = load_effective_config(cwd=cwd, home=home, env={})
            api_url = FIXED_API_URL
            default_model = (fields.get("default_model") or [""])[0].strip() or DEFAULT_MODEL
            api_key = (fields.get("api_key") or [""])[0].strip()
            if not api_key and not existing.get("apiKey"):
                config = dict(existing)
                config["apiUrl"] = api_url
                config["model"] = default_model
                self.send_html(400, setup_form_html(config=config, token=token, error_message="API Key 必填。"))
                return

            configure_values(
                cwd=cwd,
                home=home,
                api_url=api_url,
                api_key=api_key or None,
                default_model=default_model,
            )
            try:
                result = preflight(cwd=cwd, home=home, env={})
            except ImageForgeError as exc:
                config = load_effective_config(cwd=cwd, home=home, env={})
                self.send_html(400, setup_form_html(config=config, token=token, error_message=redact(str(exc))))
                return

            state["completed"] = True
            state["result"] = result
            self.send_html(200, setup_success_html(result))
            shutdown_thread = threading.Thread(target=self.server.shutdown)
            shutdown_thread.daemon = True
            shutdown_thread.start()

    server = HTTPServer((host, int(port)), SetupHandler)
    actual_host, actual_port = server.server_address[:2]
    setup_url = "http://{0}:{1}/setup?token={2}".format(
        actual_host,
        actual_port,
        parse.quote(token),
    )
    return server, setup_url, state


def run_setup_server(cwd=None, home=None, port=0, open_browser=True, timeout_seconds=900, output_func=None, open_func=None):
    output_func = output_func or print
    open_func = open_func or webbrowser.open
    server, setup_url, state = create_setup_server(cwd=cwd, home=home, port=port)
    output_func(json.dumps({
        "status": "setup_server_started",
        "url": setup_url,
        "message": "打开这个本地地址配置 ImageForge。保存后服务会自动关闭。",
    }, indent=2, sort_keys=True))
    sys.stdout.flush()
    if open_browser:
        try:
            state["browserOpened"] = bool(open_func(setup_url))
        except Exception:
            state["browserOpened"] = False

    timer = None
    if timeout_seconds and timeout_seconds > 0:
        timer = threading.Timer(timeout_seconds, server.shutdown)
        timer.daemon = True
        timer.start()
    try:
        server.serve_forever()
    finally:
        if timer:
            timer.cancel()
        server.server_close()

    if not state["completed"]:
        raise ImageForgeError("setup_timeout", "ImageForge 配置页超时，配置尚未保存。")
    return state["result"]


def ensure_ready(cwd=None, home=None, env=None, setup_func=None):
    cwd = cwd or os.getcwd()
    home = home or os.path.expanduser("~")
    try:
        return preflight(cwd=cwd, home=home, env=env)
    except ImageForgeError as exc:
        if exc.code != "missing_config":
            raise
    setup_func = setup_func or run_setup_server
    setup_func(cwd=cwd, home=home)
    return preflight(cwd=cwd, home=home, env=env)


def resolve_api_key_for_configure(api_key, prompt_func=None):
    if api_key is not None:
        stripped = api_key.strip()
        if stripped:
            return stripped
    if prompt_func is not None:
        prompted = prompt_func("ImageForge API key: ")
        if prompted is None:
            return None
        prompted = prompted.strip()
        return prompted or None
    if sys.stdin.isatty():
        prompted = getpass.getpass("ImageForge API key: ")
        return prompted.strip() or None
    return None


def default_run_git(args, cwd):
    return subprocess.check_output(["git"] + list(args), cwd=cwd, stderr=subprocess.STDOUT).decode("utf-8")


def write_version_state(path, data):
    try:
        write_json(path, data)
    except Exception:
        pass


def unavailable_version_state(checked_at):
    return {
        "status": "unavailable",
        "error": "version_check_unavailable",
        "message": VERSION_CHECK_UNAVAILABLE_MESSAGE,
        "checkedAt": checked_at,
    }


def version_unavailable(path, now, exc):
    result = unavailable_version_state(now)
    write_version_state(path, result)
    return result


def is_unavailable_version_state(state):
    return state.get("status") == "unavailable" or state.get("error") == "version_check_unavailable"


def check_version(cwd=None, ttl_hours=24, run_git=None):
    cwd = cwd or os.getcwd()
    run_git = run_git or default_run_git
    state_path = os.path.join(cwd, ".image-forge", "version-check.json")
    now = int(time.time())
    if ttl_hours > 0 and os.path.exists(state_path):
        try:
            state = read_json(state_path)
            checked_at = int(state.get("checkedAt", 0))
            if now - checked_at < ttl_hours * 3600:
                if is_unavailable_version_state(state):
                    state = unavailable_version_state(checked_at)
                    write_version_state(state_path, state)
                state["cached"] = True
                return state
        except Exception:
            pass
    try:
        local = run_git(["rev-parse", "HEAD"], cwd).strip()
        remote_raw = run_git(["ls-remote", "origin", "HEAD"], cwd).strip()
        remote = remote_raw.split()[0]
    except Exception as exc:
        return version_unavailable(state_path, now, exc)

    if local != remote:
        status = "update_available"
        upgrade = "npx skills update image-forge"
    else:
        status = "up_to_date"
        upgrade = ""
    result = {
        "status": status,
        "local": local,
        "remote": remote,
        "upgradeCommand": upgrade,
        "checkedAt": now,
    }
    write_version_state(state_path, result)
    return result


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="image_forge.py")
    subparsers = parser.add_subparsers(dest="command")

    configure_parser = subparsers.add_parser("configure")
    configure_parser.add_argument("--api-url")
    configure_parser.add_argument("--api-key")
    configure_parser.add_argument("--default-model", default=DEFAULT_MODEL)
    configure_parser.add_argument("--print-effective-config", action="store_true")

    doctor_parser = subparsers.add_parser("doctor")
    doctor_parser.add_argument("--json", action="store_true")

    subparsers.add_parser("preflight")
    subparsers.add_parser("setup")
    setup_server_parser = subparsers.add_parser("setup-server")
    setup_server_parser.add_argument("--port", type=int, default=0)
    setup_server_parser.add_argument("--no-open", action="store_true")
    setup_server_parser.add_argument("--timeout-seconds", type=int, default=900)

    ensure_ready_parser = subparsers.add_parser("ensure-ready")
    ensure_ready_parser.add_argument("--port", type=int, default=0)
    ensure_ready_parser.add_argument("--no-open", action="store_true")
    ensure_ready_parser.add_argument("--timeout-seconds", type=int, default=900)

    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--prompt", required=True)
    generate_parser.add_argument("--model")
    generate_parser.add_argument("--size", default=DEFAULT_SIZE)
    generate_parser.add_argument("--quality")
    generate_parser.add_argument("--n", type=int, default=1)
    generate_parser.add_argument("--output-dir")
    generate_parser.add_argument("--output-name")
    generate_parser.add_argument("--brief")
    generate_parser.add_argument("--direct", action="store_true")

    edit_parser = subparsers.add_parser("edit")
    edit_parser.add_argument("--image", action="append", required=True)
    edit_parser.add_argument("--prompt", required=True)
    edit_parser.add_argument("--model")
    edit_parser.add_argument("--size", default=DEFAULT_SIZE)
    edit_parser.add_argument("--output-dir")
    edit_parser.add_argument("--output-name")
    edit_parser.add_argument("--brief")
    edit_parser.add_argument("--direct", action="store_true")

    check_version_parser = subparsers.add_parser("check-version")
    check_version_parser.add_argument("--ttl-hours", type=int, default=24)

    return parser.parse_args(argv)


def print_json(data):
    print(json.dumps(data, indent=2, sort_keys=True))


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if args.command == "configure":
            api_key = resolve_api_key_for_configure(args.api_key)
            result = configure_values(
                cwd=os.getcwd(),
                home=os.path.expanduser("~"),
                api_url=args.api_url,
                api_key=api_key,
                default_model=args.default_model,
            )
            if args.print_effective_config:
                effective_config = load_effective_config()
                effective_config["apiKey"] = "configured" if effective_config.get("apiKey") else "missing"
                result["effectiveConfig"] = effective_config
            print_json(result)
            return 0
        if args.command == "doctor":
            print_json(doctor())
            return 0
        if args.command == "preflight":
            print_json(preflight())
            return 0
        if args.command == "setup":
            print_json(setup_interactive())
            return 0
        if args.command == "setup-server":
            print_json(run_setup_server(
                port=args.port,
                open_browser=not args.no_open,
                timeout_seconds=args.timeout_seconds,
            ))
            return 0
        if args.command == "ensure-ready":
            print_json(ensure_ready(
                cwd=os.getcwd(),
                home=os.path.expanduser("~"),
                env=os.environ,
                setup_func=lambda cwd, home: run_setup_server(
                    cwd=cwd,
                    home=home,
                    port=args.port,
                    open_browser=not args.no_open,
                    timeout_seconds=args.timeout_seconds,
                ),
            ))
            return 0
        if args.command == "generate":
            env = dict(os.environ)
            if args.model:
                env["IMAGE_FORGE_MODEL"] = args.model
            result = generate_image(
                prompt=args.prompt,
                size=args.size,
                quality=args.quality,
                n=args.n,
                output_dir=args.output_dir,
                output_name=args.output_name,
                env=env,
                brief=args.brief,
                direct=args.direct,
            )
            print_json({"outputs": result})
            return 0
        if args.command == "edit":
            env = dict(os.environ)
            if args.model:
                env["IMAGE_FORGE_MODEL"] = args.model
            result = edit_image(
                image_paths=args.image,
                prompt=args.prompt,
                size=args.size,
                output_dir=args.output_dir,
                output_name=args.output_name,
                env=env,
                brief=args.brief,
                direct=args.direct,
            )
            print_json({"outputs": result})
            return 0
        if args.command == "check-version":
            print_json(check_version(cwd=os.getcwd(), ttl_hours=args.ttl_hours))
            return 0
        raise ImageForgeError("missing_config", "Choose a command: ensure-ready, setup-server, setup, configure, doctor, preflight, generate, edit, or check-version")
    except ImageForgeError as exc:
        print_json({"error": exc.code, "message": redact(str(exc))})
        return 2


if __name__ == "__main__":
    sys.exit(main())
