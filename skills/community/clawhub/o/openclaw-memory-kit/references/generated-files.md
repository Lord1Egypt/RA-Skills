# Generated Files

The bootstrap script writes the following structure under the target root.

```text
<target-root>/
  .env
  .env.example
  openclaw.json
  package.json
  package-lock.json
  start-gateway.cmd
  start-gateway.ps1
  memory/
    lancedb-pro/
  workspace/
    agents/
      <role>/
        AGENTS.md
        SOUL.md
        HEARTBEAT.md
        USER.md
        MEMORY.md
    shared/
      AGENT-COLLABORATION.md
      MEMORY-SYSTEM.md
      TASK-INTAKE-RULES.md
      TASK-OBSERVABILITY.md
      TASK-SYSTEM.md
      TASK-FILE-TEMPLATE.md
      data/
        memory-mirror/
      projects/
      tasks/
        pending/
        pending-confirmation/
        in-progress/
        review/
        blocked/
        completed/
      templates/
```

## Important Generated Runtime Files

- `openclaw.json`
  Sanitized OpenClaw config with multi-agent defaults, memory scopes, gateway settings, and memory plugin configuration. The generated config uses `plugins.load.paths`, `plugins.slots.memory`, and `plugins.entries.memory-lancedb-pro.config`, which matches the current OpenClaw plugin layout while still resolving the state-local memory plugin package.

- `.env.example`
  Placeholder environment variables only. Never replace this with a copied secret-bearing file from another machine.

- `.env`
  Created from the example file if missing so the target user can fill in their own values.

- `package.json` and `package-lock.json`
  Written when core memory dependencies are installed. The kit uses state-local `openclaw` plus `memory-lancedb-pro` packages so the memory plugin can resolve `openclaw/plugin-sdk` on the current tested OpenClaw release.

- `start-gateway.ps1` and `start-gateway.cmd`
  Launchers that pin `OPENCLAW_STATE_DIR` and `OPENCLAW_CONFIG_PATH` to the generated kit instead of the user's existing default OpenClaw state.

## Optional Follow-Ups

Optional plugin installs are intentionally left out of the base scaffold. If the user explicitly asks, add commands such as:

- `openclaw plugins install @larksuite/openclaw-lark@2026.3.25 --pin`
- `openclaw plugins install @icesword760/openclaw-wechat@2026.2.24 --pin`
- `openclaw plugins install @memtensor/memos-cloud-openclaw-plugin@0.1.10 --pin`

On current OpenClaw builds, Feishu may already be bundled. Use the manual Feishu install only when the target build does not already include it.

Those package versions were the public npm versions verified from this machine on 2026-03-24.
