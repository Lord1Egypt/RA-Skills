# Security Policy

## Reporting a Vulnerability

If you believe you've found a security issue in InvestorClaw, please
email &lt;jperlow@gmail.com&gt; rather than opening a public issue.
Coordinated disclosure helps keep users safe while a fix is prepared.

A useful report typically includes:

- The version of `mnemos-os/mnemos-ic-runtime` and the
  `ghcr.io/argonautsystems/ic-engine:*` image tag in use
- A concise description of what you observed
- Reproduction steps or proof-of-concept
- Logs or `docker inspect` output that helps validate the issue

We acknowledge reports promptly, investigate in good faith, and
coordinate disclosure timing with reporters.

## Coordinated disclosure timeline

For high-severity issues we will:

1. Acknowledge within 5 business days
2. Confirm reproduction within 10 business days where possible
3. Coordinate a fix timeline with the reporter
4. Credit the reporter in `CHANGELOG.md` (with their permission) when
   the fix ships

## Scope

In scope:

- The `mnemos-ic-runtime` Docker image (bridge code, dashboard,
  Dockerfile)
- The `ghcr.io/argonautsystems/ic-engine:*` image
- The bundled `compose.yml`, `install.yaml`, and `SKILL.md`
- Per-runtime install paths under `agent-skills/**`

Out of scope (please report to the upstream maintainers):

- The `argonautsystems/ic-engine` Python source — file at
  https://github.com/argonautsystems/ic-engine/issues
- Third-party providers the engine talks to (Together AI, Finnhub,
  Massive, etc.) — see their respective security pages

## Security posture

InvestorClaw is built around a tight, minimal-surface security model:

- **Localhost-only by default.** The MCP server and dashboard bind
  exclusively to `127.0.0.1` — no external network surface.
- **Read-only by design.** InvestorClaw never executes trades, moves
  money, or authenticates to any brokerage account. It analyzes
  broker-export files the user voluntarily places in the portfolio
  directory.
- **Deterministic computation.** All portfolio math runs in
  Python — never an LLM — so numerical results are reproducible and
  auditable. The signed envelope underlying every response carries an
  HMAC fingerprint that proves the response came from the engine,
  not a fabricated source.
- **Non-root container.** The engine process runs as `uid=1000(ic)`
  inside the container, not root.
- **API keys stay local.** Provider keys persist to `/data/keys.env`
  (mode 0600) inside a named Docker volume — managed via the
  allowlisted `portfolio_keys_set` / `portfolio_keys_delete` REST
  endpoints, never logged in plain text.
- **Image pinned by digest.** `compose.yml` references the engine
  image by sha256 digest, guaranteeing reproducible builds even if
  the tag is later mutated.
- **Open-source + auditable.** Bridge / Dockerfile / dashboard /
  tests are Apache 2.0; distribution-edge artifacts (`SKILL.md`,
  `compose.yml`, `install.yaml`, `agent-skills/**`) are MIT-0. Every
  file can be reviewed before deployment.
- **Data flow control.** The user controls what leaves the machine.
  No telemetry, no analytics, no phone-home. With a local LLM
  endpoint configured, no prompt or envelope leaves the local
  network. See [`PRIVACY.md`](PRIVACY.md) for the full data-flow
  matrix.

## Hardening for shared / production deployments

The defaults above suit single-user installs on a personal machine.
For shared or production deployments, consider:

- Run the host with regular OS-level patching and a host firewall
  that allows only the loopback interface to reach `:18090` / `:18092`
- For remote access, front the service with Tailscale / nginx + mTLS
  / your VPN of choice — InvestorClaw stays bound to loopback inside
  the container
- Rotate `TOGETHER_API_KEY` (and other provider keys) regularly via
  `portfolio_keys_set`
- Pin to the sha256 digest in `compose.yml` (default) and
  re-validate the digest when upgrading
- Review `compose.yml` and `SKILL.md` before each install — both are
  intentionally short and human-readable
