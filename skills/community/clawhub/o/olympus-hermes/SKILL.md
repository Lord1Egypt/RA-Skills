---
name: ask-sources
version: 0.4.0
description: Ask Olympus for cited answers, check source readiness, and ask a frontier model anonymously through the exact four-tool Hermes MCP surface.
tools:
  - source_answer
  - source_answer_result
  - source_index_status
  - ask_anonymously
mutating: true
---

# Ask Sources from Hermes

Use `source_answer` for questions grounded in Olympus-indexed sources. Preserve
the returned citations and coverage gaps. Set `include_secure_local: true` only
when the user asks for private material and the installed sovereignty posture
has an approved analyst route for it. Do not replace an Olympus refusal with
shell, database, filesystem, browser, or provider-CLI access.

If `source_answer` returns `"status": "working"` with a `job_id`, the answer is
still being prepared and keeps running. Call `source_answer_result` with that
`job_id`, again while it says working, and deliver the answer it returns. Do
not ask the same question again.

Use `source_index_status` only for aggregate readiness and coverage checks. It
does not browse or return source content.

Use `ask_anonymously` only when the user asks to ask something anonymously,
privately or "through Olympus zkAPI". Only the question goes out, paid from
their zkAPI balance. The first time it returns `needs_choice`: ask the user
once whether they want Strict (their own model rewrites the question into
general questions first) or Standard (their words, prepared as they chose),
then call again with `level` and `remember: true`. Give the reply; when
`rewritten` is true, say so and offer to show `sent`. The result names the
`model` that answered: never one from the provider hosting the agent, and a
one-off `model` from that provider is refused. A `working` result is
collected with `source_answer_result`, like an answer.

This Hermes adaptation intentionally has no search, locator, sync, watch or
export tool. The one side-effecting tool is `ask_anonymously`: it spends from
the user's zkAPI balance, sends their question to a provider, and with
`remember: true` saves their choice; never call it unasked. If the four
declared tools are unavailable, say that the Olympus MCP lane is unavailable
and stop.
