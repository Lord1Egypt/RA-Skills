#!/usr/bin/env python3
"""Noveum integration completeness report card.

Queries recent traces for a project and grades what the integration actually
captures, using the attribute vocabulary real noveum-trace integrations emit
(manual context managers, LangChain/LangGraph, CrewAI, LiveKit, Pipecat).

Usage:
    NOVEUM_API_KEY=nv_... python check_integration.py --project my-app
    ... --voice                 # voice app: latency telemetry becomes REQUIRED
    ... --org-slug my-org       # also report the onboarding milestone
    ... --limit 50              # traces to sample (default 25)

Exit codes: 0 all required checks pass · 1 gaps found · 2 config/connectivity error.
Stdlib only; read-only (GET requests).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_ENDPOINT = "https://api.noveum.ai/api"
REQUEST_TIMEOUT_S = 30
# 25 traces is enough to see structure without heavy payloads; raise via --limit.
DEFAULT_SAMPLE = 25

# Known attribute variants per capability (union of what SDK versions/integrations emit).
LLM_MODEL_KEYS = ("llm.model",)
TOKEN_KEYS = (
    "llm.total_tokens", "llm.input_tokens", "llm.output_tokens",
    "llm.usage.total_tokens", "llm.usage.input_tokens",
    "metrics_collected.metrics.total_tokens",
)
INPUT_CONTENT_KEYS = (
    "llm.input.messages", "llm.input", "llm.chat_ctx",
    "llm.conversation.history", "turn.user_input",
)
OUTPUT_CONTENT_KEYS = ("llm.output.response", "llm.response", "tts.input_text")
SYSTEM_PROMPT_KEYS = ("llm.system_prompt",)
TOOL_KEYS_PREFIXES = ("llm.tools", "llm.function_calls", "tool.", "llm.available_tools")
TURN_KEYS = ("turn.number",)
VOICE_LATENCY_KEYS = (
    "tts.time_to_first_byte_ms", "stt.first_text_latency_ms", "stt.vad_to_final_ms",
    "turn.user_bot_latency_seconds", "llm.time_to_first_token_ms",
)
PROVENANCE_KEYS = ("code.file.path", "code.filepath")


def api_get(endpoint: str, api_key: str, path: str, params: dict) -> dict:
    qs = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{endpoint}{path}" + (f"?{qs}" if qs else "")
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_S) as res:
        return json.loads(res.read().decode(errors="replace"))


def extract_traces(payload: dict) -> list:
    # Tolerate response-envelope differences across API versions.
    for key in ("traces", "data", "results"):
        v = payload.get(key)
        if isinstance(v, list):
            return v
        if isinstance(v, dict) and isinstance(v.get("traces"), list):
            return v["traces"]
    return []


def span_attr_keys(trace: dict) -> set:
    keys: set = set()
    for span in trace.get("spans") or []:
        attrs = span.get("attributes") or {}
        if isinstance(attrs, str):
            try:
                attrs = json.loads(attrs)
            except json.JSONDecodeError:
                continue
        keys.update(attrs.keys())
    return keys


def matches(keys: set, wanted: tuple) -> bool:
    for w in wanted:
        if w.endswith("."):
            if any(k.startswith(w) for k in keys):
                return True
        elif w in keys:
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", required=True)
    ap.add_argument("--voice", action="store_true", help="require voice latency telemetry")
    ap.add_argument("--org-slug", default=None, help="also report onboarding milestone")
    ap.add_argument("--limit", type=int, default=DEFAULT_SAMPLE)
    args = ap.parse_args()

    api_key = os.environ.get("NOVEUM_API_KEY", "").strip()
    if not api_key:
        print("CONFIG ERROR: set NOVEUM_API_KEY.")
        return 2
    endpoint = os.environ.get("NOVEUM_ENDPOINT", DEFAULT_ENDPOINT).rstrip("/")

    try:
        # Live-validated query params: size / from / includeSpans (camelCase).
        payload = api_get(
            endpoint, api_key, "/v1/traces",
            {"project": args.project, "size": args.limit, "includeSpans": "true",
             "sort": "start_time:desc"},
        )
    except urllib.error.HTTPError as e:
        print(f"API ERROR: HTTP {e.code} querying traces — "
              f"{'bad key' if e.code == 401 else e.read().decode(errors='replace')[:400]}")
        return 2
    except urllib.error.URLError as e:
        print(f"NETWORK ERROR reaching {endpoint}: {e.reason}")
        return 2

    traces = extract_traces(payload)
    print(f"Noveum integration report card — project '{args.project}' "
          f"({len(traces)} recent traces sampled)\n")

    if not traces:
        print("FAIL  traces-arriving: no traces found for this project.")
        print("      → verify-traces.md 'Common failures': flush/shutdown, endpoint, key.")
        return 1

    # Aggregate over the sample.
    all_keys: set = set()
    per_trace_keys = []
    session_ids = 0
    svc_versions = 0
    error_traces = 0
    for t in traces:
        keys = span_attr_keys(t)
        per_trace_keys.append(keys)
        all_keys |= keys
        meta = t.get("metadata") or {}
        if t.get("session_id") or (isinstance(meta, dict) and meta.get("session_id")):
            session_ids += 1
        # The SDK writes the literal "unknown" when no version was configured.
        if t.get("service_version") not in (None, "", "unknown"):
            svc_versions += 1
        if t.get("status") == "error":
            error_traces += 1

    def pct(wanted: tuple) -> int:
        n = sum(1 for keys in per_trace_keys if matches(keys, wanted))
        return round(100 * n / len(per_trace_keys))

    uses_tools = matches(all_keys, TOOL_KEYS_PREFIXES)
    has_turns = matches(all_keys, TURN_KEYS)

    checks = []  # (required, name, ok, detail, fix_hint)
    checks.append((True, "llm-spans", matches(all_keys, LLM_MODEL_KEYS),
                   f"llm.model on {pct(LLM_MODEL_KEYS)}% of traces",
                   "wrap LLM calls — integrate-openai-manual.md §2"))
    checks.append((True, "token-usage", matches(all_keys, TOKEN_KEYS),
                   f"token attrs on {pct(TOKEN_KEYS)}% of traces",
                   "call capture_response()/set_usage_attributes()"))
    checks.append((True, "message-content",
                   matches(all_keys, INPUT_CONTENT_KEYS) and matches(all_keys, OUTPUT_CONTENT_KEYS),
                   f"input {pct(INPUT_CONTENT_KEYS)}% / output {pct(OUTPUT_CONTENT_KEYS)}%",
                   "capture messages + response (LLM-judge scorers need content)"))
    checks.append((False, "system-prompt", matches(all_keys, SYSTEM_PROMPT_KEYS),
                   f"llm.system_prompt on {pct(SYSTEM_PROMPT_KEYS)}% of traces",
                   "set llm.system_prompt — NovaPilot prompt fixes depend on it"))
    grouping_ok = has_turns or session_ids > 0
    checks.append((False, "conversation-grouping", grouping_ok,
                   f"turn structure: {'yes' if has_turns else 'no'}; "
                   f"session_id on {round(100 * session_ids / len(traces))}% of traces",
                   "set session_id per conversation (request-per-turn apps)"))
    if uses_tools:
        checks.append((False, "tool-telemetry", True, "tool attributes present", ""))
    checks.append((args.voice, "voice-latency", matches(all_keys, VOICE_LATENCY_KEYS),
                   f"voice latency attrs on {pct(VOICE_LATENCY_KEYS)}% of traces",
                   "install STT/TTS wrappers (LiveKit) / attach observer (Pipecat)"))
    checks.append((False, "service-version", svc_versions == len(traces),
                   f"service_version on {round(100 * svc_versions / len(traces))}% of traces",
                   "set NOVEUM_SERVICE_VERSION to the release/commit"))
    checks.append((False, "provenance", matches(all_keys, PROVENANCE_KEYS),
                   "code.file.path attrs "
                   + ("present" if matches(all_keys, PROVENANCE_KEYS) else "absent (needs newer SDK)"),
                   ""))

    failures = 0
    for required, name, ok, detail, hint in checks:
        if ok:
            status = "PASS "
        elif required:
            status = "FAIL "
            failures += 1
        else:
            status = "WARN "
        line = f"{status} {name}: {detail}"
        if not ok and hint:
            line += f"\n       → {hint}"
        print(line)

    print(f"\nINFO  error traces in sample: {error_traces} "
          "(errors being captured is good signal, not a failure)")

    if args.org_slug:
        try:
            ob = api_get(endpoint, api_key, "/v1/onboarding/status",
                         {"organizationSlug": args.org_slug})
            data = ob.get("data") or ob
            step = data.get("currentStep")
            prog = data.get("traceProgress") or {}
            print(f"INFO  onboarding milestone: {step}"
                  + (f" (traces {prog.get('count')}/{prog.get('threshold')})" if prog else ""))
        except Exception as e:  # informational only — never fail the card on this
            print(f"INFO  onboarding status unavailable: {e}")

    if failures:
        print(f"\nRESULT: {failures} required check(s) failing — integration NOT complete.")
        return 1
    print("\nRESULT: required checks pass. Review WARNs with the user before closing out.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
