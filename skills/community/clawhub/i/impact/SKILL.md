---
name: impact
description: Analyze code-change blast radius with the impact CLI. Use when reviewing diffs, assessing merge or deployment risk, finding affected tests, diffing public contracts, visualizing callers, detecting orphan code, or writing PR/MR impact summaries.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - impact
        - git
    homepage: https://github.com/nano-harness/impact-analyzer
---

# Impact

Use `impact` to explain how code changes affect callers, tests, and public contracts. It supports Go, Java, JavaScript, TypeScript, Rust, and Python. Go has deeper type-aware analysis; other languages primarily use syntax-based analysis.

Impact analyzes repositories but does not edit source code. Treat its risk classification as review guidance, not proof that a change is safe.

## Install from source

Requires Go 1.25 or newer:

```bash
git clone https://github.com/nano-harness/impact-analyzer.git
cd impact-analyzer
make build
mkdir -p ~/.local/bin
install -m 755 ./bin/impact ~/.local/bin/impact
```

Run from the target repository root and ensure Git history containing the comparison ref is available.

## Default review workflow

1. Analyze the change:

   ```bash
   impact analyze --diff HEAD~1
   ```

   For a pull request, use `origin/main...HEAD` or another explicit base ref.

2. Review breaking and warning results, then identify affected tests:

   ```bash
   impact test --diff HEAD~1
   ```

3. When public APIs, routes, CLI commands, or RPC contracts matter, run:

   ```bash
   impact surface --diff HEAD~1
   ```

4. If a structured review description is useful:

   ```bash
   impact cr --diff origin/main...HEAD
   ```

5. Add business context and run relevant tests. Do not replace human review with the tool output.

## Common commands

| Goal | Command |
|---|---|
| Analyze a diff | `impact analyze --diff <ref>` |
| Analyze dependents of one file | `impact analyze --file <path>` |
| Limit caller traversal | `impact analyze --diff <ref> --depth 5` |
| Emit JSON | `impact analyze --diff <ref> --format json` |
| Emit compact LLM context | `impact analyze --diff <ref> --format llm-context --max-tokens 4000` |
| Find affected tests | `impact test --diff <ref>` |
| Print a targeted test command | `impact test --diff <ref> --print-command` |
| Annotate with existing Go coverage | `impact test --diff <ref> --use-coverage coverage.out` |
| Diff public contracts | `impact surface --diff <ref>` |
| Filter contracts by kind | `impact surface --diff <ref> --kind cli_command,http_route` |
| Show callers of a symbol | `impact graph --symbol "pkg.Function"` |
| Show file dependencies | `impact graph --file <path>` |
| Show reverse file dependencies | `impact graph --file <path> --reverse` |
| Find potentially unreachable code | `impact orphan --min-confidence medium` |
| Diagnose setup | `impact doctor` |

Use `--lang go|java|javascript|typescript|rust|python` when automatic language detection is incorrect. Use `--index-dir <dir>` or `INDEX_CACHE_DIR` when the default `.impact/cache` should live outside the repository.

## Interpret results

- **Breaking**: a public contract or signature changed, or the change has other high-impact callers. Review all affected call sites.
- **Warning**: internal behavior changed with callers or meaningful reach. Verify behavior and tests.
- **Safe**: no significant impact was detected. This is not a correctness guarantee.
- **Orphan candidates**: potentially unreachable code, with confidence levels. Dynamic entry points can cause false positives.

Coverage annotations do not filter the affected-test list; they describe whether existing coverage reaches a test. Syntax-based call graphs may over- or under-approximate dynamic behavior. If deep Go analysis reports an error, Impact may degrade to shallower analysis; surface warnings when interpreting the result.

## Configuration

Create `.impact.yaml` only when the defaults need adjustment:

```yaml
language: go
exclude:
  - "vendor/**"
  - "tools/**"
analyze:
  depth: 5
  stop_at_entry_points: true
analysis:
  trace_affected_contracts: true
  trace_max_depth: 8
```

Keep configuration changes with the code they affect so reviewers can reproduce the analysis.

## Agent guidelines

- Prefer explicit diff refs over assuming the current branch or base.
- Use JSON for automation and `llm-context` for compact review input.
- Report empty results and degraded analysis honestly; do not invent affected files or tests.
- For orphan cleanup, inspect candidates before deleting anything.
- Do not include proprietary source code or credentials when forwarding analysis output to another service.
