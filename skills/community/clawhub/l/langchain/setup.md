# Setup — LangChain

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

LangChain moves fast and most published code is written against a version that no longer exists. Be concrete about which version an API belongs to, prefer the smallest abstraction that solves the problem, and name the cost of the loop before recommending an agent.

## How To Load Preferences

1. Read `~/Clawic/data/langchain/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `lc_version_line: 1.x`, `chat_provider: openai`, `vector_store: chroma`, `python_runtime: 3.11+`, `async_style: sync`, `tracing: none`, `trace_pii: redact`, `structured_output_method: tool_calling`.
3. Read `~/Clawic/data/langchain/memory.md` for prior context (their app shape, recurring pain points). Absence is fine; proceed without comment.
4. If the working directory contains a lockfile or requirements file, the versions there beat the configured `lc_version_line` — the installed code is the ground truth.

Work from defaults immediately. Never open with questions about their stack, providers, or how much detail they want.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a provider, vector store, Python version, or version line → update the matching key in `~/Clawic/data/langchain/config.yaml`.
- User expresses a habit or stance (where prompts live, LangGraph vs plain LCEL, approval before destructive tools, cost ceilings, citation requirements) → record it under the relevant preference area (tooling, conventions, platform, safety posture, cost posture, retrieval conventions, output format) in `~/Clawic/data/langchain/memory.md`.
- User corrects earlier guidance → update the stored value so you do not repeat it.

If the user has said nothing, store nothing. Never store API keys, endpoints with credentials, or prompt content containing customer data.

## What Memory Holds

See `memory-template.md` for the file format. Track the shape of their app (script, service, worker, notebook), which parts exist already (retrieval, agents, evals), pain points raised, and how much explanation they want with code — but only from what they actually reveal.
