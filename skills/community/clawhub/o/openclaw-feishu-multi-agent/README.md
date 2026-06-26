# OpenClaw Feishu Multi-Agent

A reusable skill for building and troubleshooting OpenClaw multi-agent collaboration on Feishu.

## What It Solves

This skill helps users set up a coordinator agent plus one or more specialist agents in a shared Feishu group, while working around the fact that Feishu bots cannot directly trigger other bots.

The core design is:

- Use Feishu `<at>` for visible mentions
- Use OpenClaw `sessions_send` for actual agent-to-agent delivery
- Let agents continue multi-hop discussions by repeating both steps on every hop

## Who It Is For

- Users who already have multiple OpenClaw agents and Feishu bots, but their routing is unstable
- Users who want to build a new multi-agent Feishu setup from scratch
- Teams that want custom role names instead of fixed presets

## Included Files

- `SKILL.md`: main usage guide
- `reference.md`: full implementation and troubleshooting guide
- `templates.md`: reusable templates
- `roles.example.json`: starter role definition
- `scripts/manage_feishu_multi_agent.py`: unified entrypoint
- `scripts/render_feishu_multi_agent.py`: generate reusable artifacts from roles
- `scripts/apply_feishu_multi_agent.py`: dry-run or apply configuration into `~/.openclaw`
- `scripts/audit_feishu_multi_agent.py`: check an existing setup against a roles file
- `scripts/repair_feishu_group_sessions.py`: repair broken Feishu group session metadata

## Typical Workflow

1. Copy `roles.example.json` to your own `roles.json`
2. Fill in your coordinator and specialist roles
3. Run `manage_feishu_multi_agent.py bootstrap` in dry-run mode
4. Review generated artifacts
5. Re-run with `--write --backup` if you want to apply to your own environment

## Why This Skill Is Different

Many Feishu multi-agent setups fail because they treat visible `@` mentions as real bot notifications. This skill makes the transport layer explicit: visual mention and internal delivery are two separate actions, and both are mandatory.

It is designed for real deployment work rather than just prompt advice: the bundle includes templates, troubleshooting docs, and scripts to render, audit, repair, and apply a multi-agent Feishu setup with a dry-run-first workflow.

## Safety

- The apply workflow defaults to dry-run
- Session repair is opt-in
- No role names are hardcoded into the architecture

## License

MIT
