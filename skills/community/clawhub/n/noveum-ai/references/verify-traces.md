# Verify the integration (acceptance gate for step 1)

Integration is **not done** when the code compiles — it is done when Noveum has received
traces and those traces carry what evals need. Missing telemetry silently poisons
downstream evals (scorers fail on absent fields, latency scorers return not-applicable),
so this gate is mandatory.

## Contents
- Local pre-check (dev mode)
- Connectivity proof (test trace)
- The completeness report card (what is checked and why)
- Reporting results
- Common failures → fixes

## 0. Local pre-check (no network, fastest loop)

Set `NOVEUM_DEV_MODE=true` and run the app once: each trace is also written as a JSON
file under `.noveum_trace_dev/`. Inspect one **selectively** (span names + attribute keys
via grep/jq — a span-heavy trace file is ~145 KB; don't read it whole). Delete the
directory afterwards; never commit it.

## 1. Prove connectivity with a known-good trace

Run: `NOVEUM_API_KEY=... NOVEUM_PROJECT=... python scripts/send_test_trace.py`

Posts one minimal valid trace to the ingest API. Failure here = key/endpoint/network,
not the SDK integration — fix that first.

## 2. Exercise the real app

Run the actual application through a few real LLM interactions. Short-lived processes
must call `noveum_trace.shutdown()` (or `flush()`) before exit or the batch is lost.

## 3. Run the completeness report card

```bash
NOVEUM_API_KEY=... python scripts/check_integration.py --project <NOVEUM_PROJECT>
# voice apps (LiveKit/Pipecat): add --voice
# to also report the onboarding milestone: add --org-slug <NOVEUM_ORG_SLUG>
```

The script queries recent traces (`GET /v1/traces?includeSpans=true`) and grades each
check. The attribute names below are what real integrations emit — the script accepts
all known variants:

| Check | Accepted signals | Why it matters |
|---|---|---|
| Traces arriving | any recent trace | Connectivity + flush working |
| LLM spans | `llm.model` on a span | Anything at all is instrumented |
| Token usage | `llm.total_tokens` / `llm.input_tokens` / `llm.usage.*` | Cost analytics, several scorers |
| Message content | `llm.input.messages` / `llm.input` / `llm.chat_ctx` / `llm.conversation.history` + `llm.output.response` / `llm.response` / `turn.user_input` | LLM-judge scorers judge content |
| System prompt | `llm.system_prompt` | NovaPilot reconstructs and fixes the prompt from this |
| Conversation grouping | `session_id` on traces, OR turn structure in one trace (`turn.number`) | Conversational scorers need turn order. **Field data: most integrations forget `session_id` — push for it in request-per-turn apps** |
| Tool telemetry | `llm.tools` / `llm.function_calls` / `tool.*` (only if the app uses tools) | Agent/tool scorers |
| Voice latency (`--voice`) | `tts.time_to_first_byte_ms`, `stt.first_text_latency_ms` / `stt.vad_to_final_ms`, `turn.user_bot_latency_seconds`, `llm.time_to_first_token_ms` | The 13 latency scorers can't measure what isn't sent |
| Service version | `service_version` set (SDK auto-fills; set `NOVEUM_SERVICE_VERSION` to your release) | Version comparison + fix verification |

Exit codes: 0 = pass · 1 = gaps found (each gap prints the reference that fixes it) ·
2 = configuration/connectivity error.

## 4. Report the result

Show the user the report card verbatim. Mark integration complete only after exit 0, or
after the user explicitly accepts named gaps (e.g. "no message content, privacy policy").
If `--org-slug` was given, report the onboarding milestone (advances at 10+ traces).

## Common failures → fixes

- **0 traces:** missing flush/shutdown; wrong `NOVEUM_ENDPOINT` (must be the API *base*,
  e.g. `https://api.noveum.ai/api` — the SDK appends `/v1/traces` itself); 401 = bad key.
- **Traces but no LLM spans:** calls bypass the handler/wrapper — grep for direct
  provider-SDK calls and wrap them (integrate-openai-manual.md §2).
- **LLM spans but no content:** `capture_response` not called / attributes not set.
- **No system prompt:** pass it explicitly (`span.set_attribute("llm.system_prompt", ...)`)
  if the framework integration doesn't capture it — NovaPilot's prompt fixes depend on it.
- **No conversation grouping:** set `session_id` (per-conversation id) in trace metadata
  for request-per-turn apps; voice frameworks already group turns within one trace.
- **No voice latency metrics:** LiveKit STT/TTS wrappers not installed, or Pipecat
  observer not attached to the task.
