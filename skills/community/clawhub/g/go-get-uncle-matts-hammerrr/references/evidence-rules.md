# Evidence Rules

## Proof Beats Claims

Use this priority order:

1. Current command output, tests, builds, live probes, registry metadata, or packaged artifacts.
2. Current source, config, scripts, CI, deployment definitions, and lockfiles.
3. Current docs and examples.
4. Memory, handoffs, old reports, comments, and summaries.

Lower-priority evidence can guide the search but cannot override higher-priority
truth.

## Evidence Requirements

- Cite exact file paths and line numbers when file evidence matters.
- Include exact commands for executable proof.
- Distinguish commands run from commands recommended but not run.
- Preserve blocked reasons: missing dependency, unsafe side effect, unavailable credentials, network disabled, external service down, or scope denied.
- Do not reveal secret values. Say the secret exists, is missing, or is referenced without printing it.

## Strong Proof

Strong proof exercises the actual public or operational behavior being claimed.
Mock-only, static-only, or unit-only proof can support a claim but cannot prove a
runtime/deployment contract by itself.
