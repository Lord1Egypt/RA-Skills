# Contributing

Thanks for improving `microsoft-365-graph-openclaw`.

## Scope

Contributions are welcome for:
- reliability and observability improvements
- documentation and onboarding quality
- security hardening and least-privilege defaults
- compatibility fixes across personal and work/school tenants

## Development basics

1) Fork and create a feature branch.
2) Keep changes focused and auditable.
3) Run local checks before opening a PR.

## Pull request guidelines

- Explain the problem and why the change is needed.
- Include test/validation steps and expected output.
- Avoid broad refactors unless directly required.
- Do not include secrets or token-bearing files.

## Security-sensitive changes

For auth, webhook, queue, or token-handling changes:
- include explicit threat/abuse considerations
- document rollback and migration steps
- update `SECURITY.md` or relevant runbooks when needed

## Documentation bar

Public-facing docs are part of product quality:
- prefer clear, operational language
- include failure modes and diagnostics
- avoid unverified claims (for example "zero cost" or "fully autonomous")
