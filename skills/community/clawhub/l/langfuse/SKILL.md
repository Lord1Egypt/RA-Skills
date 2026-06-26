---
name: langfuse
description: Query and manage Langfuse traces, prompts, datasets, sessions, observations, scores, and metrics via Langfuse SDKs and the public API. Use when setting up or auditing Langfuse tracing in cloud or self-hosted deployments, migrating hardcoded prompts into Langfuse prompt management, attaching evaluation scores or feedback, querying Langfuse data for debugging or analytics, or building Langfuse-backed workflows in Python or JS/TS projects.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "env": ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_BASE_URL"],
          },
        "primaryEnv": "LANGFUSE_SECRET_KEY",
      },
  }
---

# Langfuse

Use this skill to integrate codebases and workflows with Langfuse, the open-source LLM engineering platform for tracing, prompt management, and evaluation.

Treat **self-hosted Langfuse** as a first-class deployment mode, not a special case. When the user mentions private infrastructure, on-prem, internal URLs, custom domains, or self-hosting, configure examples and guidance around their deployment URL and platform compatibility.

Prefer SDK-based examples for Python and JS/TS. Use the public API when the task is language-agnostic, needs direct HTTP examples, or fits an existing automation pipeline.

## Quick Decision Tree

1. **Migrating hardcoded prompts into Langfuse?**
   - Read `references/prompt-migration.md`.
   - Create prompts in Langfuse, replace inline prompt literals with fetch/render calls, and preserve variable semantics.

2. **Adding observability/tracing to an app or agent?**
   - Read `references/tracing-and-querying.md`.
   - Prefer native SDK instrumentation and OpenTelemetry-compatible patterns over bespoke logging.

3. **Querying traces, observations, scores, sessions, or metrics?**
   - Read `references/tracing-and-querying.md`.
   - Use high-performance `api.observations`, `api.scores`, and `api.metrics` namespaces in current SDKs.

4. **Adding evaluation scores, feedback, or custom quality checks?**
   - Read `references/evals-and-scores.md`.
   - Attach scores at the right level: trace, observation, session, or dataset run.

5. **Working in a self-hosted Langfuse environment?**
   - Read `references/self-hosted.md` and `references/tracing-and-querying.md`.
   - Replace cloud defaults with the real deployment URL, verify platform/SDK compatibility, and avoid examples that silently assume EU cloud.

6. **Creating datasets or experiment-oriented evaluation workflows?**
   - Read `references/evals-and-scores.md`.
   - Use Langfuse datasets and dataset items where repeatable testing matters.

## Core Rules

- Prefer **Langfuse SDKs** for application integration work.
- Prefer **current SDK namespaces**:
  - Python SDK v4 / JS/TS SDK v5 use `api.observations`, `api.scores`, and `api.metrics` as the default high-performance resources.
  - Legacy v1 endpoints live under `api.legacy.*`.
- Prefer **`get_prompt` / `getPrompt`** for runtime prompt fetching to benefit from caching, retries, and fallbacks.
- Prefer **OpenTelemetry ingestion/instrumentation** over older bespoke ingestion patterns when setting up tracing.
- Keep examples small and production-usable. Do not generate giant framework-specific abstractions unless asked.
- When migrating prompts, preserve behavior first; optimize prompt structure second.
- When self-hosted is in play, do not leave cloud-region defaults in code snippets or docs. Use the deployment URL explicitly.
- Only ask for Langfuse credentials and base URL when the task actually needs live access to a Langfuse project. For design-only or code-only work, prefer placeholders or existing environment references instead of requesting secrets.

## Authentication and Environment

This skill may require these environment variables for live Langfuse access:

```bash
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_BASE_URL="https://cloud.langfuse.com"
```

Possible base URLs include:

- `https://cloud.langfuse.com` for EU Cloud
- `https://us.cloud.langfuse.com` for US Cloud
- self-hosted deployment URL when applicable, for example `https://langfuse.internal.example.com`

For self-hosted environments, prefer examples like:

```bash
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_BASE_URL="https://langfuse.internal.example.com"
```

For direct API examples, use Basic Auth with:

- username = public key
- password = secret key

## Secret-handling rules

- Prefer existing environment variables over asking the user to paste keys into chat.
- If live credentials are needed, recommend least-privilege or scoped project keys.
- Do not request production keys for read-only design or documentation tasks.
- Treat internal/self-hosted base URLs as sensitive infrastructure context and only use them for the Langfuse task at hand.

## Self-Hosted Defaults

When the user is self-hosting Langfuse:

1. Ask for or detect the actual base URL.
2. Update all code snippets and env examples to use that URL.
3. Check whether the installed SDK generation matches the self-hosted Langfuse platform version.
4. Avoid mixing `LANGFUSE_HOST` and `LANGFUSE_BASE_URL` casually; prefer the current documented variable in examples.
5. Treat self-hosted network reachability, TLS, reverse proxy paths, and auth configuration as likely failure points.

See `references/self-hosted.md`.

## Common Task Patterns

### 1. Migrate prompts into Langfuse

Use when the user says things like:

- migrate our prompts to Langfuse
- move hardcoded prompts into Langfuse prompt management
- version prompts centrally
- replace inline prompts with Langfuse fetches

Default workflow:

1. Find hardcoded prompt strings or message arrays.
2. Normalize prompt names and variable placeholders.
3. Create prompt definitions in Langfuse.
4. Replace inline prompt literals in code with Langfuse fetch/render calls.
5. Keep runtime behavior equivalent.
6. If possible, link prompt usage to traces.

See `references/prompt-migration.md`.

### 2. Add tracing / observability

Use when the user says things like:

- instrument this agent/app with Langfuse
- trace LLM calls
- add observability to prompt/model execution
- inspect sessions, generations, spans, or costs

Default workflow:

1. Identify the execution boundary: request, conversation, workflow, or agent run.
2. Decide what should be traces vs observations/spans/generations.
3. Add SDK instrumentation with stable identifiers where possible.
4. Include useful attributes: user, session, tags, model, latency, token/cost-relevant data.
5. Verify resulting traces are queryable.

See `references/tracing-and-querying.md`.

### 3. Query data for debugging or analytics

Use when the user asks to:

- inspect traces or observations
- pull sessions or scores
- build analysis scripts on Langfuse data
- generate reports from Langfuse metrics

Default workflow:

1. Use direct entity APIs for individual data retrieval.
2. Use the Metrics API for aggregated counts, costs, token usage, or grouped reporting.
3. Paginate explicitly.
4. Select only the fields needed.

See `references/tracing-and-querying.md`.

### 4. Add evaluations and scores

Use when the user asks to:

- score traces or outputs
- collect user feedback
- implement guardrails or quality checks
- attach custom eval results to traces or sessions

Default workflow:

1. Choose the score target: trace, observation, session, or dataset run.
2. Choose the score type: numeric, categorical, or boolean.
3. Use stable score names and comments.
4. Keep score semantics consistent across runs.

See `references/evals-and-scores.md`.

### 5. Adapt work for self-hosted Langfuse

Use when the user says things like:

- we run Langfuse on-prem
- we are self-hosting Langfuse
- use our internal Langfuse URL
- this is not cloud.langfuse.com
- make this work behind our private domain or proxy

Default workflow:

1. Replace cloud URLs with the real deployment URL.
2. Verify environment-variable naming and SDK initialization for the target stack.
3. Check platform/SDK compatibility if behavior looks incomplete or broken.
4. Keep examples deployment-agnostic except for the explicit base URL.
5. Flag infra issues separately from application-instrumentation issues.

See `references/self-hosted.md`.

## Output Expectations

When doing Langfuse work, produce one or more of:

- code patches for Python or JS/TS integration
- prompt migration plans with explicit before/after mapping
- small utility scripts for querying or migrating data
- API examples with auth and payload shape
- concise runbooks for how to verify Langfuse behavior
- self-hosted deployment-aware env/config examples when applicable

## References

- `references/prompt-migration.md` — prompt management and migration patterns
- `references/tracing-and-querying.md` — observability, querying, traces, observations, sessions, metrics
- `references/evals-and-scores.md` — scores, feedback, datasets, evaluation workflows
- `references/self-hosted.md` — self-hosted deployment guidance, compatibility, and env/config rules

## Coverage check against Langfuse's own skill/docs

This skill intentionally covers the main workflows Langfuse advertises for coding agents:

- setting up Langfuse tracing in a project
- auditing existing instrumentation
- migrating prompts to Langfuse prompt management
- querying traces, prompts, datasets, and related entities via SDK/API
- looking up Langfuse integration and usage patterns
- adapting integrations for self-hosted Langfuse deployments

If the request becomes very framework-specific, keep this skill as the Langfuse layer and combine it with the relevant coding/framework skill rather than bloating this skill with per-framework boilerplate.
