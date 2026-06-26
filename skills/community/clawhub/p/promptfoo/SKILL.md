---
name: promptfoo
description: Work with Promptfoo for local, repeatable LLM evals and red-team testing. Use when a request explicitly involves Promptfoo, `promptfooconfig.yaml`, Promptfoo CLI commands (`promptfoo eval`, `validate`, `view`, `redteam`, `generate`, `mcp`), Promptfoo examples, assertions/metrics, provider comparisons, RAG evals, agent evals, or converting an LLM app/API workflow into Promptfoo-based quality or security tests. Do not trigger for generic prompt-writing alone unless the task specifically needs Promptfoo.
---

# Promptfoo

Use Promptfoo when the task is specifically about Promptfoo-based evals, regression suites, or red-team scans.

## Trigger boundaries

Trigger this skill for:

- `promptfooconfig.yaml` creation or editing
- Promptfoo CLI usage
- Promptfoo assertions and metrics
- provider/model comparisons through Promptfoo
- Promptfoo evals for RAG, agents, or API-backed systems
- Promptfoo red-team configuration and reporting
- Promptfoo MCP server setup

Do not trigger this skill for:

- generic prompt engineering with no Promptfoo requirement
- general LLM benchmarking discussions with no Promptfoo workflow
- one-off model questions that do not need a repeatable eval harness

## Repo-aligned config idioms

Promptfoo examples consistently use these patterns:

- schema header:

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
```

- top-level `description`
- `prompts`, `providers` and/or `targets`
- `tests` with `vars`
- optional `defaultTest.assert`
- `file://...` references for prompts, docs, agents, tools, or local files

Use Promptfoo's idioms directly instead of inventing a custom layout.

## Quick decision tree

Choose the workflow that matches the request:

- **Create a first config or example suite** → use `promptfoo init` or the helper scripts in `scripts/`
- **Check or fix a config** → inspect `promptfooconfig.yaml`, then run `promptfoo validate`
- **Compare prompts or providers** → use `promptfoo eval`
- **Inspect historical runs, logs, or outputs** → use `promptfoo list`, `promptfoo show`, `promptfoo logs`, `promptfoo view`
- **Generate adversarial tests or security scans** → use `promptfoo redteam ...`
- **Generate datasets or assertions** → use `promptfoo generate ...`
- **Expose Promptfoo to an MCP-compatible toolchain** → use `promptfoo mcp`

## Default workflow

1. Find or create `promptfooconfig.yaml`
2. Make the config look like Promptfoo's real examples, not an invented abstraction
3. Validate before expensive runs
4. Run a narrow eval first
5. Review failures in CLI or web view
6. Tighten prompts, assertions, or test cases
7. Re-run at broader scale

Prefer small, representative suites before big fan-out runs.

## Config shapes that match Promptfoo examples

### 1. Basic getting-started shape

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Getting started

prompts:
  - 'Convert the following English text to {{language}}: {{input}}'

providers:
  - openai:gpt-5.2
  - openai:gpt-5-mini

tests:
  - vars:
      language: French
      input: Hello world
    assert:
      - type: contains
        value: 'Bonjour le monde'
```

### 2. Shared assertions with `defaultTest`

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Automatic response evaluation using LLM rubric scoring

prompts:
  - file://prompts.txt

providers:
  - openai:chat:gpt-5.2

defaultTest:
  assert:
    - type: llm-rubric
      value: Do not mention that you are an AI or chat assistant

tests:
  - vars:
      name: Bob
      question: Can you help me find a specific product on your website?
```

### 3. RAG eval shape

```yaml
# yaml-language-server: $schema=https://promptfoo.dev/config-schema.json
description: Evaluating RAG responses using multiple quality metrics

prompts:
  - |
    You are an internal corporate chatbot.
    Respond to this query: {{query}}
    Here is some context that you can use to write your response: {{context}}

providers:
  - openai:gpt-4.1-mini

tests:
  - vars:
      query: What is the max purchase that doesn't require approval?
      context: file://docs/reimbursement.md
    assert:
      - type: contains
        value: '$500'
      - type: factuality
        value: the employee's manager is responsible for approvals
      - type: answer-relevance
        threshold: 0.9
      - type: context-faithfulness
        threshold: 0.9
```

### 4. Agent eval shape

Promptfoo supports richer provider objects for agent systems:

```yaml
providers:
  - id: openai:agents:my-agent
    config:
      agent: file://./agents/my-agent.ts
      tools: file://./tools/my-tools.ts
      maxTurns: 20
```

Use provider objects like this when evaluating agent workflows instead of flattening everything into plain prompt strings.

## Assertion strategy

Use the simplest assertion that reliably captures the requirement.

Prefer, roughly in this order:

1. deterministic assertions such as `contains`, `icontains`, `regex`, `contains-any`, `is-json`, `latency`, `cost`
2. focused model-assisted assertions such as `llm-rubric`, `factuality`, `answer-relevance`, `context-faithfulness`, `context-recall`, `context-relevance`
3. `javascript` or `python` assertions when built-ins are insufficient
4. `assert-set` when you need grouped pass criteria

Guidance:

- Use deterministic checks for formatting, policy phrases, JSON shape, tool mentions, and hard constraints
- Use RAG metrics for groundedness instead of forcing one vague rubric to do everything
- Use `contains-any` or `contains-all` when wording can vary but key content must appear
- Use `javascript` for custom logic only when a built-in metric does not fit
- If an assertion flakes, tighten the test or use a more appropriate metric

## Prompt and provider eval workflow

### 1. Start from reality

If Promptfoo already has a relevant example, use it as the base:

```bash
npx promptfoo@latest init --example getting-started
npx promptfoo@latest init --example eval-rag
npx promptfoo@latest init --example compare-openai-models
```

If the task matches one of the helper scripts in `scripts/`, use the script to scaffold a repo-aligned starter config quickly.

### 2. Validate

```bash
npx promptfoo@latest validate
```

If the config is not in the current directory, pass the correct path.

### 3. Run a narrow eval first

```bash
npx promptfoo@latest eval
npx promptfoo@latest eval --filter-first-n 5
npx promptfoo@latest eval --filter-pattern "refund|billing"
npx promptfoo@latest eval --filter-providers "openai|anthropic"
npx promptfoo@latest eval --max-concurrency 4
```

Use filters for large or expensive suites.

### 4. Review and iterate

```bash
npx promptfoo@latest view
npx promptfoo@latest list evals
npx promptfoo@latest show <eval-id>
npx promptfoo@latest logs
```

Focus on:

- repeated failures across one provider
- prompt-specific regressions
- flaky assertions
- cost or latency regressions
- app-path failures hidden by toy prompt-only tests

## RAG and agent evaluation guidance

For RAG:

- use realistic retrieved context
- prefer `file://...` documents when the source material is local
- use `factuality`, `answer-relevance`, `context-recall`, `context-relevance`, and `context-faithfulness` where appropriate
- keep at least some deterministic assertions for hard facts

For agents:

- test tool-use behavior, not just surface prose
- include assertions for tool mentions, valid outputs, or trajectory/tool behavior if traces are available
- use provider objects and file-backed agent/tool definitions when that mirrors the real app

## Red-team workflow

Use this when the goal is jailbreak testing, prompt injection resistance, policy enforcement, data exposure checks, or broader AI vulnerability scanning.

### Fast path

```bash
npx promptfoo@latest redteam setup
npx promptfoo@latest redteam run
npx promptfoo@latest redteam report
```

### No-GUI path

```bash
npx promptfoo@latest redteam init --no-gui
```

### What to define carefully

For red-team configs, pay special attention to:

- `purpose` - what the system does, who the legitimate user is, and what must stay protected
- `targets` - HTTP endpoint, model provider, custom script, or direct app integration
- plugin selection - select the relevant attack classes instead of blindly enabling everything
- strategy selection - increase sophistication only as needed

Use stable target labels over time so reports stay comparable.

### Review checklist

After a scan, summarize:

- which vulnerability classes failed
- severity and reproducibility
- exact broken policy or trust boundary
- whether mitigations belong in prompts, retrieval, app logic, tool permissions, or filters
- which failures should become normal regression tests

Do not leave red-team results as a one-off report. Convert serious failures into permanent eval coverage.

## Useful CLI commands

```bash
npx promptfoo@latest init
npx promptfoo@latest init --example getting-started
npx promptfoo@latest init --example eval-rag
npx promptfoo@latest init --example compare-openai-models
npx promptfoo@latest validate
npx promptfoo@latest eval
npx promptfoo@latest eval --resume
npx promptfoo@latest eval --retry-errors
npx promptfoo@latest list evals
npx promptfoo@latest show <eval-id>
npx promptfoo@latest logs
npx promptfoo@latest view
npx promptfoo@latest generate dataset
npx promptfoo@latest generate assertions
npx promptfoo@latest redteam setup
npx promptfoo@latest redteam run
npx promptfoo@latest redteam report
npx promptfoo@latest mcp --transport stdio
```

## Cost and speed hygiene

Promptfoo can fan out quickly. Keep it under control.

- start with a narrow provider set
- start with a small test sample
- cap concurrency when providers are rate-limited
- use cache unless fresh outputs are required
- use `--retry-errors` for transient failures
- use `--resume` for interrupted longer runs

## Troubleshooting

If an eval behaves strangely:

1. run `promptfoo validate`
2. check env vars and provider credentials
3. reduce to one provider and one test
4. inspect logs with `promptfoo logs`
5. verify prompt variable names match test `vars`
6. check whether assertions match the actual output shape
7. verify whether the real app path should be tested via `targets` instead of a toy prompt string

Common failure classes:

- missing API keys or wrong provider syntax
- tests using vars not referenced by prompts
- brittle assertions on non-deterministic outputs
- excessive concurrency causing rate limits
- evaluating a simplified prompt instead of the real app

## Bundled helpers

Use these helper scripts when they fit:

- `scripts/scaffold-promptfoo-config.py` - generate repo-aligned starter configs for common modes
- `scripts/promptfoo-preflight.py` - inspect a Promptfoo workspace and suggest the next command

## References

Read these as needed:

- `references/config-patterns.md` for repo-aligned templates and selection heuristics
- `references/example-notes.md` for patterns observed in Promptfoo's own examples
