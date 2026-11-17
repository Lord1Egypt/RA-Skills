---
name: mcp-token-lab
description: Generate or edit importable multi-plan JSON templates for MCP Token Lab to compare AI agent workflows, MCP tool-schema loading, on-demand discovery, prefix caching, context compression, token usage, model costs, and estimated latency. Use for agent scenario modeling and strategy comparisons; not for live model calls or general JSON conversion.
---

# MCP Token Lab: Strategy Comparisons

Given a user's agent workflow and comparison goals, deliver a UTF-8 `.json` file with a template name, template description, and descriptions of each plan. The web app simulates scenarios locally in the browser without an API key. A configuration stores experiment settings, not simulation results.

## Generate or modify a scenario

1. Read the [import format contract](references/import-format.md). Identify the number of turns, Skills/Tools counts, context sizes, model-call sequence, caching, compression, pricing, and step durations. When neither the user nor an existing configuration specifies values, default to **100 turns, 100 Tools, and a 100K-token compression threshold in TOKEN mode**. Ask about material business differences when necessary; otherwise proceed with clearly labeled numeric assumptions.
2. Read only the examples relevant to the request from the table below and adapt them. Typically create 2–8 plans; a single plan is valid when explicitly requested. Hold turn counts, tool-result sizes, model prices, and corresponding step durations constant across plans, varying only the experiment's target factors unless the user specifically requests other differences. When editing a configuration, preserve unrelated settings and metadata.
3. Supply the complete configuration and execution flows according to the contract. Ensure that global inheritance flags do not unintentionally override plan-specific values. Include descriptions for new templates and each plan; plan descriptions may interpolate actual parameters using `{{variableName}}`, as defined in the contract. Preserve the source of model prices supplied by the user or the existing configuration. Check official prices only if the user requests current pricing; otherwise identify unknown rates as assumptions.
4. Validate the result using the instructions below. Deliver the JSON file link, a summary of differences between plans, and key assumptions. Include this UI path: **Web app → Templates → Import custom template → Select JSON → Use template**. Applying a template replaces the current configuration and can be undone. If the user explicitly requests a plain configuration, return only the inner `config` object and explain that it does not include a template title or introduction. If the user requests raw JSON, output valid JSON only.

## Choose a scenario example

| Goal | Reference file | Focus |
| --- | --- | --- |
| Simple two-plan comparison or no matching scenario | [Two-plan example](assets/comparison.example.json) | Full schema preloading versus on-demand schema discovery; uses the Skill's default scale |
| Tool-loading strategies without compression | [progressive-tool-no-compress](assets/examples/progressive-tool-no-compress.json) | Full preload, Hosted Tool Search, and progressive loading; 25 turns |
| Tool-loading strategies with standard compression | [progressive-tool-100k](assets/examples/progressive-tool-100k.json) | The same three strategies; 100 turns, 100K threshold |
| Higher compression threshold | [progressive-tool-200k](assets/examples/progressive-tool-200k.json) | The same three strategies; 100 turns, 200K threshold |
| Tool-search approaches | [tool-search](assets/examples/tool-search.json) | Full preload versus Regex, BM25, and Semantic Top-5 search |
| Tool namespaces and frequently used tools | [tool-namespace-hybrid](assets/examples/tool-namespace-hybrid.json) | Flat preload, namespaces, and pinned + on-demand tools; interval triggers |
| Smaller tool results | [tool-result-shaping](assets/examples/tool-result-shaping.json) | Raw results, field projection, and batched aggregation |

All six packaged built-in examples are fully importable templates that can be used independently of the web app. They retain the web scenarios' values, including **120 Tools**; use their execution flows as references by default, without overriding the generation defaults above. When the user explicitly asks to reproduce a built-in scenario, retain its parameters. If modifying turns, tool counts, or thresholds, update descriptions and dependent variables consistently. The no-compression scenario achieves its behavior by using a TURN threshold greater than the total turn count; adjust that threshold when increasing turns. Example pricing may be historical snapshots or illustrative assumptions, not live quotes. Durations are estimates and do not establish equivalent model quality or actual billed costs.

## Validation and maintenance

When the target repository source and dependencies are available, **run full simulation and strict validation** from the repository root before delivering a generated file:

```bash
node skills/mcp-token-lab/scripts/validate-config.mjs --repo . <output-file.json> --simulate --strict
```

This validator reuses the application's importer and simulation engine rather than defining a competing schema. `--simulate` evaluates all turns; `--strict` rejects unresolved variables, unsupported description expressions, and unmatched double braces. Files must not exceed 4 MB. Without the repository source or dependencies, check JSON syntax, documented fields, inheritance, variables, and flow structure; explicitly state that import compatibility and full simulation have not been verified.

When maintaining packaged built-in examples, treat `src/config/default-template/` as the source of truth; do not edit generated files under `assets/examples/` directly. Synchronize from the repository root:

```bash
node skills/mcp-token-lab/scripts/sync-builtins.mjs --repo .
```

Add `--check` to verify synchronization without writing files. `pnpm test` also verifies example synchronization and runs strict validation and full simulation for every example.
