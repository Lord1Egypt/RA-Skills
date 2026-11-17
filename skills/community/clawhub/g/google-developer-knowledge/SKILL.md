---
name: google-developer-knowledge
description: "Retrieve current, source-backed official Google developer documentation for Google Cloud, Firebase, Android, Google AI, Gemini CLI, Flutter, Go, Maps, Web, TensorFlow, and related products. Use for setup, migrations, troubleshooting, architecture, and code examples when current Google documentation matters."
metadata:
  openclaw:
    emoji: "☁️"
    requires:
      bins:
        - mcporter
        - jq
        - curl
  related-skills:
    mcporter: to discover and call a Google Developer Knowledge-capable MCP server.
---

# Google Developer Knowledge — Official Google Docs Skill

Use this skill when the task needs current official Google developer documentation for Google Cloud, Firebase, Android, Google AI, Gemini CLI, Flutter, Go, Maps, Web, TensorFlow, or other products indexed by the Developer Knowledge corpus.

## Core Rule

Use `mcporter` capability discovery from `references/mcporter-workflow.md`. Select only a healthy server exposing Google Developer Knowledge search, full-document retrieval, and grounded-answer capabilities. Do not assume a server alias, URL, tool-name prefix, authentication arrangement, or native tool wrapper.

## Tool Choice

1. Start with `search_documents` for most research. It returns official documentation chunks with `parent`, `id`, and `content`.
2. Use `get_documents` with returned `parent` document names when snippets are insufficient or citations need full-page context.
3. Use `answer_query` for a quick grounded synthesis only when its references are sufficient. If it returns 429, times out, or lacks adequate references, fall back to `search_documents` plus `get_documents`.

## Decision Checkpoints

1. **🔴 CHECKPOINT — Capability discovery:** Parse the selected route returned by discovery into `gdk_server`, `gdk_search_tool`, `gdk_get_tool`, and `gdk_answer_tool`. If discovery finds no compatible server, record the reason and use REST only with `DEVELOPERKNOWLEDGE_API_KEY` or OAuth credentials plus a quota project; otherwise use an official-document fallback.
2. **🔴 CHECKPOINT — Evidence sufficiency:** For version-sensitive, pricing, quota, security, or migration claims, retrieve the relevant full document with `get_documents`. A search snippet or an `answer_query` response alone is not enough.
3. **🔴 CHECKPOINT — Retrieval budget:** Retrieve no more than three parent documents by default. Ask before broad extraction, offline use, or a larger document set.
4. **🔴 CHECKPOINT — Output trace:** State the selected server or fallback, the retrieval method, and source URLs or document URIs. If the needed detail is absent, mark it unverified rather than infer it.

## Quick Commands

```bash
# Run capability discovery from references/mcporter-workflow.md first.
gdk_route='<selected-route-json>'
gdk_server="$(jq -r '.server' <<<"$gdk_route")"
gdk_search_tool="$(jq -r '.tools.search' <<<"$gdk_route")"
gdk_get_tool="$(jq -r '.tools.get' <<<"$gdk_route")"
gdk_answer_tool="$(jq -r '.tools.answer' <<<"$gdk_route")"

mcporter call "$gdk_server.$gdk_search_tool" \
  --args '{"query":"Cloud Run minimum instances concurrency pricing"}' \
  --output json

mcporter call "$gdk_server.$gdk_get_tool" \
  --args '{"names":["documents/docs.cloud.google.com/run/docs/about-concurrency"]}' \
  --output json

mcporter call "$gdk_server.$gdk_answer_tool" \
  --args '{"query":"Compare Cloud Run and Cloud Functions for a new HTTP microservice."}' \
  --output json
```

## Workflow

1. Define one focused documentation question.
2. Pass Capability discovery and retain the returned route and tool names for the task.
3. Search with `search_documents`.
4. Pull the best `parent` documents with `get_documents` when evidence requires full context.
5. Pass Evidence sufficiency, then synthesize only from retrieved evidence.
6. Pass Retrieval budget and Output trace before responding.

## Coverage and Limits

- Corpus covers public pages from Google developer domains such as `cloud.google.com`, `docs.cloud.google.com`, `firebase.google.com`, `developer.android.com`, `ai.google.dev`, `developers.google.com`, `web.dev`, `go.dev`, `docs.flutter.dev`, and `www.tensorflow.org`.
- Some generated API reference prefixes are excluded from the corpus, especially language-specific Google Cloud reference directories.
- Data freshness target is usually 24-48 hours after documentation publication.
- Full documents are Markdown and can be large; retrieve only the pages needed for the answer.

## Detailed Reference

Use `references/mcporter-workflow.md` for command patterns, field shapes, troubleshooting, and source-backed answer patterns.

Use `references/api-fallback.md` only after capability discovery fails, when validating a client integration, or when the task specifically asks for direct Developer Knowledge REST API calls. Never attempt REST without an API key or OAuth credentials plus a quota project.

## Retrieval Record

For answers that depend on current Google behavior, include a concise record:

- `method`: `mcp`, `rest-api-key`, `rest-oauth`, or `official-document`.
- `server`: selected MCP server, or `none` when fallback was used.
- `fallback_reason`: `none`, discovery failure, rate limit, authentication failure, or corpus gap.
- `sources`: official URLs or document URIs used.
- `verification`: `full-document`, `search-snippet-only`, or `unverified`.

## Anti-Patterns

| Do not | Why | Correct action |
| --- | --- | --- |
| Hardcode a server alias or endpoint | Server names and authentication differ between runtimes. | Use capability discovery and retain the selected `gdk_server` for the task. |
| Treat a search snippet or unreferenced synthesis as proof | It can omit constraints or be stale for consequential claims. | Fetch the parent document and cite its URI before making the claim. |
| Retry timeout, rate-limit, or authentication errors without a bound | It hides an integration failure and can amplify requests. | Follow the Failure Matrix: one bounded 429 retry, then fallback or stop. |
| Call REST without an API key or OAuth token plus quota project | It creates a predictable authentication or quota failure. | Use REST only after an authentication preflight; otherwise use official Google documentation. |
| Claim a grounded answer after MCP or retrieval fails | The result is no longer evidence-backed. | State the fallback reason and mark unavailable details as unverified. |
| Send sensitive, proprietary, or credential material in documentation queries | Queries can leave the current environment. | Use product names, public error text, and minimal non-sensitive context only. |

## Official Documents

These are the official documents this skill was built from:

- `https://developers.google.com/knowledge/api`
- `https://developers.google.com/knowledge/quickstart`
- `https://developers.google.com/knowledge/howto`
- `https://developers.google.com/knowledge/answer-query`
- `https://developers.google.com/knowledge/mcp`
- `https://developers.google.com/knowledge/reference/mcp`
- `https://developers.google.com/knowledge/reference/mcp/tools_list/search_documents`
- `https://developers.google.com/knowledge/reference/mcp/tools_list/answer_query`
- `https://developers.google.com/knowledge/reference/mcp/tools_list/get_documents`
- `https://developers.google.com/knowledge/reference/corpus-reference`
