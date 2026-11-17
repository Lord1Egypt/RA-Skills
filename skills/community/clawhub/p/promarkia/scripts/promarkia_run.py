#!/usr/bin/env python3
"""Promarkia marketing client with versioned authorization safeguards."""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


SKILL_VERSION = "1.2.0"
CONTRACT_VERSION = 2
_ALLOWED_HOSTS = {"www.promarkia.com", "promarkia.com"}
_ALLOWED_SQUADS = {
    "9": ("Image Creator", "marketing image generation and editing"),
    "10": ("Video Squad", "marketing video creation and rendering"),
    "11": ("Social Media", "social drafting or confirmed publishing"),
    "12": ("Copywriting", "marketing copy drafting or confirmed publishing"),
    "16": ("SEO Expert", "keyword, SERP, and on-page analysis"),
    "17": ("Campaign Planner", "campaign planning and channel strategy"),
    "18": ("Digital Ads", "advertising creative and reporting drafts"),
    "21": ("Lead Generation", "prospect research or confirmed outreach"),
}
_EXTERNAL_CAPABLE_SQUADS = frozenset({"11", "12", "21"})
_LEGACY_SAFE_DRAFT_SQUADS = frozenset({"9", "10", "16", "17"})
_TASK_MODES = frozenset({"draft-only", "external-action"})
_EXTERNAL_ACTIONS = frozenset(
    {
        "comment",
        "contact",
        "email",
        "forward",
        "invite",
        "message",
        "outreach",
        "post",
        "publish",
        "reply",
        "send",
        "share",
        "upload",
    }
)
_DRAFT_MODE_CONTRADICTION_RE = re.compile(
    r"\b(publish(?:es|ed|ing)?|send(?:s|ing)?|sent|message(?:s|d|ing)?|"
    r"email(?:s|ed|ing)?|upload(?:s|ed|ing)?|outreach|contact(?:s|ed|ing)?|"
    r"invite(?:s|d|ing)?|comment(?:s|ed|ing)?|repl(?:y|ies|ied|ying)|"
    r"forward(?:s|ed|ing)?|share(?:s|d|ing)?|activate(?:s|d|ing)?)\b|"
    r"\bpost(?:s|ed|ing)?\s+(?:it|this|that|the|to|on)\b",
    re.IGNORECASE,
)
_PERSISTENCE_RE = re.compile(
    r"\b(?:cron|recurr(?:ing|ence|ent|s)?|schedul(?:e|es|ed|ing)|"
    r"repeat(?:s|ed|ing)?\s+(?:automatically|daily|weekly|monthly|hourly)|"
    r"auto(?:mate|mates|mated|mating|matically)|auto[- ]?(?:post|publish|send|upload)|"
    r"every\s+(?:hour|day|week|month|monday|tuesday|wednesday|thursday|friday|"
    r"saturday|sunday)|(?:post|publish|send|upload|message|email|run)\s+"
    r"(?:later|tomorrow|tonight|next\s+(?:hour|day|week|month))|"
    r"(?:queue|defer)(?:s|red|ring|d|ing)?\b[\s\S]{0,80}\b(?:for|until|at|on)\b|"
    r"(?:go\s+live|deliver)\b[\s\S]{0,60}\b(?:later|tomorrow|tonight|after|"
    r"next\s+(?:hour|day|week|month)|at|on)\b|"
    r"(?:post|publish|send|upload|message|email|run)\b[\s\S]{0,40}\b"
    r"(?:at\s+\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)?|"
    r"on\s+\d{4}-\d{2}-\d{2}))",
    re.IGNORECASE,
)
_RESERVED_AUTH_MARKER_RE = re.compile(
    r"PROMARKIA_AUTHORIZATION_V\d+|TASK_MODE\s*:", re.IGNORECASE
)
_RUN_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_TOOLKIT_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{1,63}$")
_ACCOUNT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,255}$")
_ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_BIDI_AND_ZERO_WIDTH = dict.fromkeys(
    map(
        ord,
        "\u061c\u200b\u200c\u200d\u200e\u200f\u202a\u202b\u202c\u202d"
        "\u202e\u2060\u2066\u2067\u2068\u2069\ufeff",
    ),
    None,
)
_MAX_PROMPT_CHARS = 12_000
_MAX_RESPONSE_BYTES = 2_000_000
_MAX_AUTH_FIELD_CHARS = 500


class PromarkiaError(RuntimeError):
    """Fatal request or validation error."""


class TransientPromarkiaError(PromarkiaError):
    """Retryable transport or server error."""


def _safe_text(value, limit=5000):
    text = str(value or "")
    text = _ANSI_RE.sub("", text).translate(_BIDI_AND_ZERO_WIDTH)
    text = "".join(ch for ch in text if ch in "\n\t" or ord(ch) >= 32)
    return text[:limit]


def _validate_api_base(raw):
    base = (raw or "").rstrip("/")
    parsed = urllib.parse.urlparse(base)
    if parsed.scheme != "https" or parsed.hostname not in _ALLOWED_HOSTS:
        raise PromarkiaError(
            "PROMARKIA_API_BASE must use HTTPS on an official Promarkia host."
        )
    try:
        parsed_port = parsed.port
    except ValueError as exc:
        raise PromarkiaError("PROMARKIA_API_BASE contains an invalid port.") from exc
    if (
        parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in ("", "/")
        or parsed_port not in (None, 443)
    ):
        raise PromarkiaError("PROMARKIA_API_BASE contains unsupported URL components.")
    return base


API_BASE = _validate_api_base(
    os.environ.get("PROMARKIA_API_BASE", "https://www.promarkia.com")
)
API_KEY = os.environ.get("PROMARKIA_API_KEY", "")


class _SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme != "https" or parsed.hostname not in _ALLOWED_HOSTS:
            raise urllib.error.HTTPError(
                newurl,
                code,
                "Blocked redirect outside official Promarkia hosts",
                headers,
                fp,
            )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_SafeRedirectHandler())


def _headers():
    if not API_KEY:
        raise PromarkiaError(
            "PROMARKIA_API_KEY is not configured in the protected skill environment."
        )
    return {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json",
        "X-Promarkia-Client": f"openclaw-skill/{SKILL_VERSION}",
    }


def _request(
    method,
    path,
    json_body=None,
    params=None,
    idempotency_key=None,
    allow_not_found=False,
):
    url = f"{API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(json_body).encode("utf-8") if json_body is not None else None
    headers = _headers()
    if idempotency_key is not None:
        headers["Idempotency-Key"] = _normalize_authorization_id(idempotency_key)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with _OPENER.open(req, timeout=120) as resp:
            final = urllib.parse.urlparse(resp.geturl())
            if final.scheme != "https" or final.hostname not in _ALLOWED_HOSTS:
                raise PromarkiaError("Response came from an untrusted host.")
            body = resp.read(_MAX_RESPONSE_BYTES + 1)
            if len(body) > _MAX_RESPONSE_BYTES:
                raise PromarkiaError("Promarkia response exceeded the 2 MB safety limit.")
            try:
                decoded = body.decode("utf-8")
                parsed_body = json.loads(decoded) if decoded.strip() else {}
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise PromarkiaError("Promarkia returned invalid JSON.") from exc
            if not isinstance(parsed_body, (dict, list)):
                raise PromarkiaError("Promarkia returned an unsupported JSON response.")
            return parsed_body
    except urllib.error.HTTPError as exc:
        if allow_not_found and exc.code == 404:
            return None
        body = exc.read(8192).decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body)
            detail = (
                parsed.get("description") or parsed.get("error") or body
                if isinstance(parsed, dict)
                else body
            )
        except (json.JSONDecodeError, ValueError):
            detail = body
        message = f"HTTP {exc.code}: {_safe_text(detail, 1000)}"
        if exc.code == 429 or exc.code >= 500:
            raise TransientPromarkiaError(message) from exc
        raise PromarkiaError(message) from exc
    except urllib.error.URLError as exc:
        raise TransientPromarkiaError(
            f"Network error: {_safe_text(exc.reason, 500)}"
        ) from exc


def _validate_run_id(run_id):
    if not _RUN_ID_RE.fullmatch(str(run_id or "")):
        raise PromarkiaError(
            "Run ID must contain only letters, digits, underscores, or hyphens."
        )


def _normalize_authorization_id(value):
    try:
        parsed = uuid.UUID(str(value or ""))
    except (ValueError, AttributeError, TypeError) as exc:
        raise PromarkiaError(
            "--authorization-id must be a UUID created for this exact approved run."
        ) from exc
    if parsed.int == 0:
        raise PromarkiaError("--authorization-id cannot be the nil UUID.")
    return str(parsed)


def _authorization_field(name, value, required=False):
    cleaned = str(value or "").strip()
    if required and not cleaned:
        raise PromarkiaError(f"--{name} is required for an external action.")
    if len(cleaned) > _MAX_AUTH_FIELD_CHARS or any(ord(ch) < 32 for ch in cleaned):
        raise PromarkiaError(
            f"--{name} must be at most {_MAX_AUTH_FIELD_CHARS} printable characters."
        )
    if _RESERVED_AUTH_MARKER_RE.search(cleaned):
        raise PromarkiaError(f"--{name} contains a reserved authorization marker.")
    return cleaned


def _parse_connector_bindings(values):
    bindings = {}
    for raw in values or []:
        if "=" not in str(raw):
            raise PromarkiaError(
                "--connector-binding must use TOOLKIT=ACCOUNT_ID format."
            )
        toolkit, account_id = str(raw).split("=", 1)
        toolkit = toolkit.strip().lower()
        account_id = account_id.strip()
        if not _TOOLKIT_RE.fullmatch(toolkit):
            raise PromarkiaError("Connector toolkit names are invalid or unsupported.")
        if not _ACCOUNT_ID_RE.fullmatch(account_id):
            raise PromarkiaError("Connector account IDs are invalid or unsupported.")
        if toolkit in bindings and bindings[toolkit] != account_id:
            raise PromarkiaError(
                f"Connector toolkit {toolkit!r} is bound to multiple account IDs."
            )
        bindings[toolkit] = account_id
    return dict(sorted(bindings.items()))


def _build_authorization_manifest(
    squad_id,
    prompt,
    timeout,
    task_mode,
    credit_confirmed,
    external_confirmed,
    authorization_id,
    external_action=None,
    external_destination=None,
    external_audience=None,
    external_toolkit=None,
    connector_bindings=None,
):
    if squad_id not in _ALLOWED_SQUADS:
        allowed = ", ".join(_ALLOWED_SQUADS)
        raise PromarkiaError(
            f"Squad {squad_id!r} is outside this marketing-only package. Allowed IDs: {allowed}."
        )
    if not prompt or len(prompt) > _MAX_PROMPT_CHARS or "\x00" in prompt:
        raise PromarkiaError(
            f"Prompt must contain 1-{_MAX_PROMPT_CHARS} characters and no NUL bytes."
        )
    if prompt.translate(_BIDI_AND_ZERO_WIDTH) != prompt:
        raise PromarkiaError(
            "The prompt contains bidi or zero-width controls that could obscure its scope."
        )
    if any(ord(ch) < 32 and ch not in "\n\r\t" for ch in prompt):
        raise PromarkiaError("The prompt contains unsupported control characters.")
    if _RESERVED_AUTH_MARKER_RE.search(prompt):
        raise PromarkiaError(
            "The prompt contains a reserved authorization marker. Remove it and retry."
        )
    if not credit_confirmed:
        raise PromarkiaError(
            "Submitting sends the prompt to Promarkia and consumes credits. Obtain "
            "current user authorization, then rerun with --confirm-credit-use."
        )
    if task_mode not in _TASK_MODES:
        raise PromarkiaError(
            "Declare --task-mode draft-only or --task-mode external-action."
        )
    normalized_authorization_id = _normalize_authorization_id(authorization_id)
    if _PERSISTENCE_RE.search(prompt):
        raise PromarkiaError(
            "Recurring, deferred, or scheduled execution is outside this skill. "
            "Use Promarkia's reviewed scheduler in a separate authorized workflow."
        )

    bindings = dict(sorted((connector_bindings or {}).items()))
    action = _authorization_field("external-action", external_action)
    destination = _authorization_field("external-destination", external_destination)
    audience = _authorization_field("external-audience", external_audience)
    toolkit = _authorization_field("external-toolkit", external_toolkit).lower()
    if task_mode == "draft-only":
        if external_confirmed or action or destination or audience or toolkit or bindings:
            raise PromarkiaError(
                "Draft-only runs cannot include external-action confirmation, metadata, "
                "or connector bindings."
            )
        if _DRAFT_MODE_CONTRADICTION_RE.search(prompt):
            raise PromarkiaError(
                "The prompt appears to request an external action but --task-mode is "
                "draft-only. Rewrite it as a draft request or obtain current confirmation."
            )
    else:
        if squad_id not in _EXTERNAL_CAPABLE_SQUADS:
            raise PromarkiaError(
                f"Squad {squad_id} is draft-only in this package and cannot perform external actions."
            )
        if not external_confirmed:
            raise PromarkiaError(
                "Obtain current user confirmation for the exact action, destination, "
                "audience, toolkit, and account, then use --confirm-external-action."
            )
        action = _authorization_field("external-action", external_action, True).lower()
        destination = _authorization_field("external-destination", external_destination, True)
        audience = _authorization_field("external-audience", external_audience, True)
        toolkit = _authorization_field("external-toolkit", external_toolkit, True).lower()
        if action not in _EXTERNAL_ACTIONS:
            allowed = ", ".join(sorted(_EXTERNAL_ACTIONS))
            raise PromarkiaError(
                f"Unsupported --external-action {action!r}. Allowed actions: {allowed}."
            )
        if not _TOOLKIT_RE.fullmatch(toolkit):
            raise PromarkiaError("--external-toolkit is invalid or unsupported.")
        if toolkit not in bindings:
            raise PromarkiaError(
                "External-action mode requires --connector-binding for the exact external toolkit."
            )

    bound_request = {
        "authorizationId": normalized_authorization_id,
        "contractVersion": CONTRACT_VERSION,
        "squadId": squad_id,
        "taskMode": task_mode,
        "prompt": prompt,
        "timeout": timeout,
        "externalAction": action or None,
        "externalDestination": destination or None,
        "externalAudience": audience or None,
        "externalToolkit": toolkit or None,
        "connectorBindings": bindings,
        "externalActionAllowed": task_mode == "external-action",
        "persistenceAllowed": False,
    }
    request_digest = hashlib.sha256(
        json.dumps(bound_request, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    manifest = {key: value for key, value in bound_request.items() if key != "prompt"}
    manifest["requestSha256"] = request_digest
    return manifest


def _authorized_prompt(prompt, manifest):
    lines = [
        "[PROMARKIA_AUTHORIZATION_V2]",
        f"authorization_id: {manifest['authorizationId']}",
        f"request_sha256: {manifest['requestSha256']}",
        f"TASK_MODE: {manifest['taskMode'].upper().replace('-', '_')}",
        "persistence_allowed: false",
    ]
    if manifest["taskMode"] == "external-action":
        bindings_json = json.dumps(
            manifest["connectorBindings"], sort_keys=True, separators=(",", ":")
        )
        lines.extend(
            [
                "external_action_allowed: true",
                f"authorized_action: {manifest['externalAction']}",
                f"authorized_destination: {manifest['externalDestination']}",
                f"authorized_audience: {manifest['externalAudience']}",
                f"authorized_toolkit: {manifest['externalToolkit']}",
                f"authorized_connector_bindings: {bindings_json}",
                "Perform only that immediate action through the bound account. Do not widen scope.",
            ]
        )
    else:
        lines.extend(
            [
                "external_action_allowed: false",
                "Produce the requested draft, analysis, or local artifact only.",
                "Do not publish, post, send, message, email, upload, contact, or schedule.",
            ]
        )
    lines.extend(["[/PROMARKIA_AUTHORIZATION_V2]", "", "USER_TASK:", prompt])
    return "\n".join(lines)


def get_capabilities():
    result = _request(
        "GET",
        "/api/external/capabilities",
        params={"client": "openclaw", "contract": CONTRACT_VERSION},
        allow_not_found=True,
    )
    if result is not None and not isinstance(result, dict):
        raise PromarkiaError("Promarkia returned an invalid capabilities response.")
    return result


def _nested_true(data, *path):
    current = data
    for key in path:
        if not isinstance(current, dict):
            return False
        current = current.get(key)
    return current is True


def _max_timeout(capabilities, squad_id):
    if not capabilities:
        return 1200
    limits = capabilities.get("maxTimeoutSeconds")
    if isinstance(limits, int):
        return limits
    if isinstance(limits, dict):
        value = limits.get(str(squad_id), limits.get("default", 1200))
        if isinstance(value, int):
            return value
    return 1200


def _validate_server_contract(capabilities, manifest):
    squad_id = manifest["squadId"]
    task_mode = manifest["taskMode"]
    timeout = int(manifest["timeout"])
    if capabilities is None:
        if task_mode == "external-action" or squad_id not in _LEGACY_SAFE_DRAFT_SQUADS:
            raise PromarkiaError(
                "Promarkia does not advertise the enforced OpenClaw v2 authorization contract. "
                "This squad or action is blocked to prevent an unbound external write."
            )
        if timeout > 1200:
            raise PromarkiaError(
                "The current Promarkia API advertises no extended timeout; use 1200 seconds or less."
            )
        return

    try:
        version = int(capabilities.get("contractVersion", 0))
    except (TypeError, ValueError):
        version = 0
    if version < CONTRACT_VERSION:
        raise PromarkiaError("Promarkia returned an unsupported external API contract version.")
    required = (
        _nested_true(capabilities, "authorization", "manifestEnforced"),
        _nested_true(capabilities, "authorization", "idempotencyBound"),
        _nested_true(capabilities, "authorization", "requestDigestEnforced"),
        _nested_true(capabilities, "taskModes", task_mode, "toolPolicyEnforced"),
    )
    if not all(required):
        raise PromarkiaError(
            "Promarkia did not confirm all required server-side authorization controls."
        )
    if task_mode == "external-action" and not all(
        (
            _nested_true(capabilities, "externalActions", "accountBindingRequired"),
            _nested_true(capabilities, "externalActions", "receiptRequired"),
        )
    ):
        raise PromarkiaError(
            "Promarkia did not confirm immutable account binding and action receipts."
        )
    allowed_squads = capabilities.get("allowedSquads")
    if isinstance(allowed_squads, list) and squad_id not in map(str, allowed_squads):
        raise PromarkiaError(f"Promarkia contract does not allow squad {squad_id}.")
    limit = _max_timeout(capabilities, squad_id)
    if timeout < 60 or timeout > limit:
        raise PromarkiaError(
            f"Timeout must be between 60 and {limit} seconds for squad {squad_id}."
        )


def list_squads():
    remote = _request("GET", "/api/external/squads")
    if not isinstance(remote, list):
        raise PromarkiaError("Promarkia returned an invalid squad list.")
    remote_by_id = {str(item.get("id")): item for item in remote if isinstance(item, dict)}
    print("Approved Promarkia marketing squads:")
    for squad_id, (name, purpose) in _ALLOWED_SQUADS.items():
        available = "available" if squad_id in remote_by_id else "not returned by account"
        print(f"  {squad_id:>2}  {name:<18} {purpose} [{available}]")


def show_capabilities():
    capabilities = get_capabilities()
    if capabilities is None:
        print("Promarkia external API contract: legacy (no v2 capability declaration).")
        print("External actions and squads 11, 12, 18, and 21 are blocked by this client.")
        return
    print("--- BEGIN UNTRUSTED PROMARKIA CAPABILITIES ---")
    print(_safe_text(json.dumps(capabilities, indent=2, sort_keys=True), 20000))
    print("--- END UNTRUSTED PROMARKIA CAPABILITIES ---")


def list_connections():
    capabilities = get_capabilities()
    try:
        version = int((capabilities or {}).get("contractVersion", 0))
    except (TypeError, ValueError):
        version = 0
    if capabilities is None or version < 2:
        raise PromarkiaError("Promarkia does not advertise the v2 connection catalog.")
    result = _request("GET", "/api/external/connections")
    connections = result.get("connections", []) if isinstance(result, dict) else []
    print("Connected accounts available to the authenticated Promarkia account:")
    for item in connections:
        if not isinstance(item, dict):
            continue
        toolkit = _safe_text(item.get("toolkit"), 80)
        account_id = _safe_text(item.get("id"), 260)
        name = _safe_text(item.get("name"), 160)
        status = _safe_text(item.get("status"), 40)
        print(f"  {toolkit:<20} {account_id:<40} {name} [{status}]")


def _find_action_receipts(result):
    keys = (
        "externalActionReceipt",
        "externalWriteReceipt",
        "publicationReceipt",
        "actionReceipt",
    )
    found = []

    def visit(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in keys and child:
                    found.append(child)
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(result)
    return found


def _display_result(result, require_external_receipt=False):
    billing = result.get("billing") if isinstance(result, dict) else None
    if isinstance(billing, dict):
        print(f"Billing status: {_safe_text(billing.get('status'), 80)}")
        if billing.get("reservedCredits") is not None:
            print(f"Reserved credits: {billing.get('reservedCredits')}")
    print(f"Credits used: {result.get('creditCost', 0)}")
    print(f"Total tokens: {result.get('totalTokens', 0)}")
    receipts = _find_action_receipts(result)
    if require_external_receipt and not receipts:
        raise PromarkiaError(
            "The run completed without an authoritative external-action receipt. "
            "Do not claim that publication or outreach succeeded."
        )
    if receipts:
        print("Authoritative external-action receipts:")
        print(_safe_text(json.dumps(receipts, indent=2, sort_keys=True), 12000))
    messages = result.get("messages", [])
    if not messages and isinstance(result.get("result"), dict):
        messages = result["result"].get("messages", [])
    rendered = []
    for msg in messages or []:
        if not isinstance(msg, dict):
            continue
        content = msg.get("content", "")
        if not isinstance(content, str) or not content.strip():
            continue
        stripped = content.strip()
        if stripped.startswith("{") and (
            '"LLMCall"' in stripped[:200] or '"tools"' in stripped[:80]
        ):
            continue
        for marker in ("TERMINATE", "PLAN_READY_ON_SCREEN", "DOCS_DONE"):
            content = content.replace(marker, "")
        content = _safe_text(content.strip())
        if content:
            rendered.append((_safe_text(msg.get("source", "unknown"), 80), content))
    print("\n--- BEGIN UNTRUSTED PROMARKIA OUTPUT ---")
    if rendered:
        for source, content in rendered:
            print(f"\n[{source}]\n{content}")
    else:
        print("No readable result content returned.")
    print("--- END UNTRUSTED PROMARKIA OUTPUT ---\n")


def list_artifacts(run_id):
    _validate_run_id(run_id)
    result = _request("GET", f"/api/runs/{run_id}/artifacts")
    artifacts = result.get("artifacts", []) if isinstance(result, dict) else []
    print(f"Artifacts for run {run_id}: {len(artifacts)}")
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        print(
            "  "
            + " | ".join(
                [
                    _safe_text(artifact.get("id"), 120),
                    _safe_text(artifact.get("file_name"), 240),
                    _safe_text(artifact.get("mime_type"), 120),
                    str(artifact.get("size_bytes", 0)),
                    _safe_text(artifact.get("status"), 40),
                ]
            )
        )


def submit_task(
    squad_id,
    prompt,
    timeout,
    task_mode,
    credit_confirmed,
    external_confirmed,
    authorization_id,
    external_action=None,
    external_destination=None,
    external_audience=None,
    external_toolkit=None,
    connector_bindings=None,
    poll_interval=10,
    no_wait=False,
    include_artifacts=False,
):
    if timeout < 60 or timeout > 7200:
        raise PromarkiaError("Timeout must be between 60 and 7200 seconds.")
    manifest = _build_authorization_manifest(
        squad_id,
        prompt,
        timeout,
        task_mode,
        credit_confirmed,
        external_confirmed,
        authorization_id,
        external_action,
        external_destination,
        external_audience,
        external_toolkit,
        connector_bindings,
    )
    capabilities = get_capabilities()
    _validate_server_contract(capabilities, manifest)
    submitted_prompt = _authorized_prompt(prompt, manifest)
    print(f"Submitting an approved task to squad {squad_id}.")
    print(f"Prompt length: {len(prompt)} characters (content is not logged).")
    print(f"Task mode: {task_mode}.")
    print(f"Authorization ID: {manifest['authorizationId']}.")
    print(f"Request SHA-256: {manifest['requestSha256']}.")
    print("Notice: the prompt is sent to Promarkia and this run consumes credits.")
    result = _request(
        "POST",
        "/api/external/tasks",
        json_body={
            "squadId": squad_id,
            "prompt": submitted_prompt,
            "timeout": timeout,
            "authorization": manifest,
            "connectorBindings": manifest["connectorBindings"],
        },
        idempotency_key=manifest["authorizationId"],
    )
    if not isinstance(result, dict):
        raise PromarkiaError("Promarkia returned an unsupported task response.")
    status = str(result.get("status", "unknown"))
    run_id = str(result.get("runId", ""))
    if run_id:
        _validate_run_id(run_id)
        print(f"Run ID: {run_id}")
    billing = result.get("billing")
    if isinstance(billing, dict) and billing.get("reservedCredits") is not None:
        print(f"Reserved credits: {billing.get('reservedCredits')}")
    if status in {"error", "failed", "cancelled"}:
        raise PromarkiaError(_safe_text(result.get("error", f"Run {status}"), 1000))
    require_receipt = task_mode == "external-action"
    if status == "completed":
        _display_result(result, require_external_receipt=require_receipt)
        if include_artifacts and run_id:
            list_artifacts(run_id)
        return
    if not run_id:
        raise PromarkiaError("Promarkia did not return a run ID for the submitted task.")
    if no_wait:
        print("Run submitted without waiting. Retrieve this run ID before retrying.")
        return
    elapsed = 0
    while elapsed < timeout:
        time.sleep(poll_interval)
        elapsed += poll_interval
        try:
            poll = _request("GET", f"/api/external/runs/{run_id}")
        except TransientPromarkiaError as exc:
            print(f"[{elapsed}s] Temporary poll error: {_safe_text(exc, 300)}")
            continue
        poll_status = str(poll.get("status", "processing"))
        if poll_status == "completed":
            print(f"Completed after approximately {elapsed}s.")
            _display_result(poll, require_external_receipt=require_receipt)
            if include_artifacts:
                list_artifacts(run_id)
            return
        if poll_status in {"error", "failed", "cancelled"}:
            raise PromarkiaError(_safe_text(poll.get("error", f"Run {poll_status}"), 1000))
        print(f"[{elapsed}s] Still processing.")
    raise PromarkiaError(
        f"Local wait timed out after {timeout}s. The remote run may still be active. "
        f"Check run {run_id} before submitting a replacement."
    )


def get_run(run_id, include_artifacts=False):
    _validate_run_id(run_id)
    result = _request("GET", f"/api/external/runs/{run_id}")
    status = str(result.get("status", "unknown"))
    print(f"Run ID: {run_id}")
    print(f"Status: {_safe_text(status, 80)}")
    authorization = result.get("authorization") or {}
    require_receipt = (
        isinstance(authorization, dict)
        and authorization.get("taskMode") == "external-action"
    )
    if status == "completed":
        _display_result(result, require_external_receipt=require_receipt)
        if include_artifacts:
            list_artifacts(run_id)
    elif status in {"error", "failed", "cancelled"}:
        print(f"Error: {_safe_text(result.get('error', f'Run {status}'), 1000)}")
    elif status in {"processing", "queued", "running"}:
        print("Task is still running. Check again later.")
    else:
        print("--- BEGIN UNTRUSTED PROMARKIA OUTPUT ---")
        print(_safe_text(json.dumps(result, default=str), 5000))
        print("--- END UNTRUSTED PROMARKIA OUTPUT ---")


def main():
    parser = argparse.ArgumentParser(
        description="Run one explicitly requested Promarkia marketing task."
    )
    parser.add_argument("--squad", "-s", help="Approved marketing squad ID")
    parser.add_argument("--prompt", "-p", help="User-approved task prompt")
    parser.add_argument("--timeout", "-t", type=int)
    parser.add_argument("--list-squads", "-l", action="store_true")
    parser.add_argument("--capabilities", action="store_true")
    parser.add_argument("--list-connections", action="store_true")
    parser.add_argument("--get-run", "-g", metavar="RUN_ID")
    parser.add_argument("--list-artifacts", metavar="RUN_ID")
    parser.add_argument("--include-artifacts", action="store_true")
    parser.add_argument("--no-wait", action="store_true")
    parser.add_argument("--task-mode", choices=sorted(_TASK_MODES))
    parser.add_argument("--authorization-id")
    parser.add_argument("--confirm-credit-use", action="store_true")
    parser.add_argument("--confirm-external-action", action="store_true")
    parser.add_argument("--external-action", choices=sorted(_EXTERNAL_ACTIONS))
    parser.add_argument("--external-destination")
    parser.add_argument("--external-audience")
    parser.add_argument("--external-toolkit")
    parser.add_argument(
        "--connector-binding",
        action="append",
        default=[],
        metavar="TOOLKIT=ACCOUNT_ID",
    )
    args = parser.parse_args()
    try:
        if args.list_squads:
            list_squads()
        elif args.capabilities:
            show_capabilities()
        elif args.list_connections:
            list_connections()
        elif args.list_artifacts:
            list_artifacts(args.list_artifacts)
        elif args.get_run:
            get_run(args.get_run, include_artifacts=args.include_artifacts)
        elif args.squad and args.prompt:
            timeout = args.timeout if args.timeout is not None else 1200
            submit_task(
                str(args.squad),
                args.prompt,
                timeout,
                args.task_mode,
                args.confirm_credit_use,
                args.confirm_external_action,
                args.authorization_id,
                args.external_action,
                args.external_destination,
                args.external_audience,
                args.external_toolkit,
                _parse_connector_bindings(args.connector_binding),
                no_wait=args.no_wait,
                include_artifacts=args.include_artifacts,
            )
        else:
            parser.print_help()
            return 2
    except PromarkiaError as exc:
        print(f"ERROR: {_safe_text(exc, 1200)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
