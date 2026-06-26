# Contributing to mnemos-ic-runtime (InvestorClaw v4.x)

InvestorClaw v4.x is split across three repositories. Pick the right
one for your contribution:

| Layer | Repository | What lives here |
|---|---|---|
| **Engine source** | [`argonautsystems/ic-engine`](https://github.com/argonautsystems/ic-engine) | Python portfolio analyzers, FINOS-CDM-inspired data model, deterministic computation |
| **Runtime + skill** (this repo) | [`mnemos-os/mnemos-ic-runtime`](https://github.com/mnemos-os/mnemos-ic-runtime) | Docker image build, MCP-HTTP bridge, dashboard, agent skill files, ClawHub-publishable distribution-edge artifacts |
| **AI primitives** | [`argonautsystems/clio`](https://gitlab.com/argonautsystems/clio) | Schema-map, normalize, vision-extract |

If you're not sure which repo your change belongs in, file an issue
here first; we'll redirect.

## At minimum

- **License compatibility** — substantive code (bridge, dashboard,
  Dockerfile, tests) must be Apache 2.0–compatible. Distribution-edge
  artifacts (`SKILL.md`, `compose.yml`, `install.yaml`,
  `agent-skills/**`) must stay MIT-0 — required by ClawHub schema.
- **Conventional Commits** — use the
  [Conventional Commits](https://www.conventionalcommits.org/) spec
  (e.g. `feat(bridge):`, `fix(skill):`, `docs:`).
- **Tests pass** — for bridge changes, the bridge unit tests under
  `bridge/` must remain green. For engine-affecting changes, the
  Agentic COBOL regression in `harness/cobol/` must hold its baseline
  pass rate (≥ 245/250).
- **Don't push directly to main** — open a PR for review. CI on the
  GitLab mirror will run lint + tests.

## Building the container locally

```bash
git clone https://github.com/mnemos-os/mnemos-ic-runtime.git
cd mnemos-ic-runtime
docker build -t ic-engine:dev --build-arg IC_ENGINE_REF=main .
```

Then test:

```bash
mkdir -p portfolios
docker run --rm -p 18090:8090 -p 18092:8092 \
  -v $(pwd)/portfolios:/data/portfolios \
  ic-engine:dev
```

## Reporting bugs and feature requests

- **Bugs**: open an issue with reproduction steps, version, and
  platform (host OS, Docker version, agent runtime).
- **Security-sensitive reports**: see [SECURITY.md](SECURITY.md) — do
  not open a public issue.
- **Feature requests**: open an issue describing the use case before
  writing code.

## Documentation contributions

Doc-only PRs are welcome. The `SKILL.md` is the agent-readable spec
that ClawHub publishes — keep its frontmatter intact and the structure
agent-friendly. The `README.md` is the human-facing entry point — keep
it concise and link out for depth.

## Architectural changes

For non-trivial architectural changes, file an RFC under
`docs/RFC-v<n>.md` first; use [`RFC-v0.1.md`](RFC-v0.1.md) as a
template. RFCs go through the same PR review as code changes.

## Commit author identity

Commit author email must match the contributor's public OSS identity.
Employer-affiliated email addresses are not appropriate for OSS
contributions to this project — use a personal address.

## Code of Conduct

All contributors are expected to follow the
[Code of Conduct](CODE_OF_CONDUCT.md) (Contributor Covenant 2.1).
