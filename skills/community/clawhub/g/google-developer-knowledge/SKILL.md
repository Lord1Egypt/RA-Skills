---
name: google-developer-knowledge
description: "Retrieve current, source-backed official Google developer documentation for Google Cloud, Firebase, Android, Google AI, Gemini CLI, Flutter, Go, Maps, Web, TensorFlow, and related products. Use for setup, migrations, troubleshooting, architecture, and code examples when current Google documentation matters."
version: 1.0.3
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

# Google Developer Knowledge — Official Google Docs Retrieval

This locally maintained skill uses Google’s official Developer Knowledge corpus. It is distinct from Google’s [`retrieving-developer-knowledge`](https://github.com/google/skills/tree/main/skills/developers/retrieving-developer-knowledge) skill.

## Workflow

1. **Discover the route.** Use [the mcporter workflow](references/mcporter-workflow.md) to select a configured server by schema. Accept direct tools or the `GoogleDeveloperKnowledge-` prefix; require search/get and treat answer as optional. Do not add an endpoint, change credentials, or start OAuth to answer a documentation question.
2. **Search first for exact details.** Use `search_documents` with a focused public question. For code, CLI flags, error messages, settings, pricing, quotas, security, and migrations, select relevant `results[].parent` values and use `get_documents` to verify the full source.
3. **Use a grounded answer for concepts when helpful.** `answer_query` returns `answerText` and references; deduplicate them and verify the relevant full sources for consequential claims. On 429, timeout, missing tool, or poor references, switch to search/get. Do not retry a quota-exhausted answer tool.
4. **Retrieve only necessary sources.** Use exact names returned by search or answer, not guessed `documents/...` paths. Fetch at most three documents by default, even though the tool supports 20 per call. Ask before broad extraction or offline use.
5. **Cite and disclose limits.** Cite the retrieved `uri` or authoritative `documents/...` name. Briefly state the route and any fallback that affected the answer; distinguish full-document verification, search snippets, grounded synthesis, and unverified claims.

## Fallbacks and scope

- If a named feature still has no relevant result after one refinement, report the corpus gap and check public official product docs. `answer_query` uses the same corpus. A transport error is not an empty result.
- Use [REST v1](references/api-fallback.md) when MCP is unavailable, direct integration is requested, or REST-only filters or pagination are necessary. Use only an already-authorized API key or OAuth token with quota project; otherwise use an official public page.
- The [corpus reference](https://developers.google.com/knowledge/reference/corpus-reference) lists covered domains and exclusions. Google targets re-indexing within 48 hours and availability within two business days; this is not a freshness guarantee. Read the release notes or current official page when the latest version matters.
- Send only public product names, error text, or other minimum non-sensitive context. Do not send credentials, private project identifiers, proprietary code, or private incident details.

The [mcporter reference](references/mcporter-workflow.md) has runnable commands, response fields, error handling, and Cloud Run, Firebase, and Firestore smoke-test results.
