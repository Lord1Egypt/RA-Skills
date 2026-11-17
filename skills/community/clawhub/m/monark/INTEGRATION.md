# Integrating the MONARK gate

MONARK is one public MCP endpoint exposing the four tools `{attest, gate, cascade, calibrate}`:

- `https://mcp.monarkgate.tech/mcp` (HTTP/JSON mirror: `POST https://api.monarkgate.tech/{attest|gate|cascade|calibrate}`)

Transport is Streamable HTTP. The endpoint is public and unauthenticated, with no availability
commitment; treat it as a reference implementation of the coverage-gate contract, not a hosted service
with an uptime promise.

## The redemption-velocity class

Besides the two built-in plumbing fixtures, this endpoint serves `stable-run-velocity-24h`: a committed
split-conformal calibration for one population (USDe), measured on calm onchain redemption-flow windows.
Every other population abstains (`under_calib`). Alongside it, an off-tool **daily** sentinel steps an
adaptive quantile tracker on the attested 24h flow and publishes a replayable timeline (`state.json`,
`timeline.jsonl`) at `monarkgate.tech/narabi/`; the committed gate region is static and does not change
until a pre-registered drift criterion fires and an ADR says so.

## One-line install

### Hermes / claw-agent

```
hermes mcp add monark --url https://mcp.monarkgate.tech/mcp
```

`hermes mcp add` takes **no `--transport` flag**: a server added with `--url` defaults to Streamable
HTTP, and the YAML `transport:` key is set separately (by editing the config or via `hermes mcp
configure`). To scope which tools are exposed, use `hermes mcp configure monark` (or the config keys
`tools.include` / `tools.exclude`). Confirm the server is reachable with `hermes mcp test monark`.

### OpenClaw

```
openclaw mcp add monark --url https://mcp.monarkgate.tech/mcp --transport streamable-http
```

Here `--transport streamable-http` is an explicit flag. Scope the exposed tools at add time with
`--include` (for example `--include 'gate,calibrate'`) or `--exclude`. Verify the wiring with
`openclaw mcp doctor monark --probe`.

## Discovery

The governed source of this skill is `skills/monark/SKILL.md` in the MONARK repository.
`.agents/skills/monark/SKILL.md` is a **consumer-side, post-install** path: an operator obtains it by
installing from ClawHub (per ClawHub's own install instructions) or by copying the source directly.
MONARK does **not** generate `.agents/skills/` in its own repository. In-repo discovery is **OpenClaw-only** (its workspace `skills/` tier is open by default);
for Hermes, and for sharing in general, the path is **ClawHub first**, then the operator installs it
(Hermes additionally requires opting the project root into `skills.trusted_project_dirs`, so the
operator stays in control of activation).

## License

This skill is licensed under **MIT-0** (MIT No Attribution); see `LICENSE`. The MONARK harness itself
is a separate, Apache-2.0 codebase.
