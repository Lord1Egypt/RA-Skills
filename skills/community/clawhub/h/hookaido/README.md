# hookaido

Agent skill for [Hookaido](https://github.com/nuetzliches/hookaido), a single-binary webhook ingress queue. The skill teaches an agent to:

- configure, run and validate Hookaido
- verify provider signatures
- deliver events durably to an OpenClaw Gateway or any other consumer
- triage queues and the DLQ

Pinned to Hookaido `v2.15.2`.

## Install

**OpenClaw / ClawHub**

```bash
openclaw skills install @7schmiede/hookaido
```

The skill's install actions download the pinned Hookaido release and verify its SHA256 before extracting it.

**Claude Code** (plugin marketplace, project or user scope)

```text
/plugin marketplace add 7schmiede/claw-skill-hookaido
/plugin install hookaido@hookaido
```

**Manual:** copy this directory to `~/.claude/skills/hookaido/`, `<workspace>/skills/hookaido/` (OpenClaw), or upload it as a skill on claude.ai.

## What's inside

- `SKILL.md`: operating guidance, safety rules, topology chooser, install metadata.
- `references/openclaw.md`: Hookaido in front of the OpenClaw Gateway. Covers push to `/hooks/<name>`, the pull relay for a Gateway behind NAT, egress setup, the security checklist, and MCP registration for OpenClaw and Claude Code.
- `references/operations.md`: install, container, and release verification, plus CLI, DSL patterns, the Pull/SSE/gRPC and Admin APIs, metrics, and secret rotation.
- `scripts/install_hookaido.sh`: fallback installer for the pinned release with SHA256 verification.
- `scripts/openclaw_pull_relay.sh`: pull relay from Hookaido to a local OpenClaw hook. It acks only after a `2xx`, sends an `Idempotency-Key`, and requires HTTPS for any non-loopback URL.
- `scripts/publish.sh`: maintainer-only ClawHub publish, with the ClawHub CLI pinned. It is excluded from the published bundle.
- `.claude-plugin/marketplace.json`: Claude Code marketplace. The entry doubles as the plugin manifest. There is deliberately no `plugin.json`, because ClawHub would then classify the repo as a plugin and refuse `clawhub publish` for the skill.

## Security notes

- Binary downloads are pinned and checksum-verified. The checksums come from the signed upstream `hookaido_v2.15.2_checksums.txt`; the signature, SBOM and provenance were checked with `hookaido verify-release`.
- The skill only talks to the operator's own Hookaido and OpenClaw endpoints.
- MCP registration is project-local and read-only by default. Mutations and DLQ deletion need explicit operator intent.

## License

MIT-0 (see `LICENSE`).
