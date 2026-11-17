# Platform Adapter Notes

OnePilot keeps one shared `SKILL.md` and one shared CLI. Platform notes only describe how an agent loads the skill, executes the CLI, and handles local scheduling or mailbox access.

Do not copy recommendation, memory, feedback, subscription, or application behavior into platform-specific files. Update `SKILL.md` and `scripts/onepilot-agent.mjs` for core behavior changes.

## Common Contract

Every compatible agent needs one of these capabilities:

- read a `SKILL.md` folder
- execute local shell commands
- install an extension/plugin that can call the CLI
- connect to a future OnePilot MCP server

Use the same helper command everywhere from the installed OnePilot CLI package root:

```bash
node ./scripts/onepilot-agent.mjs status
```

For platforms that launch commands from another working directory, the wrapper should first resolve the installed CLI package root, then call `scripts/onepilot-agent.mjs` inside it. Do not hard-code Codex paths in shared instructions.

For event recommendations, ask the user whether a local schedule/calendar tool is available and whether they agree to let the agent read availability. Only read free/busy information after agreement. If no tool is available or the user declines, collect availability conversationally.

## Codex

- Install into `$HOME/.codex/skills/onepilot`.
- Codex can read `SKILL.md` directly.
- Shared examples use `node ./scripts/onepilot-agent.mjs`; in Codex this means commands are run from `$HOME/.codex/skills/onepilot`.
- Use `--agent-name Codex` when binding.
- If Gmail connector is available, read the OnePilot verification code through Gmail and pass it to `bind-email verify --code-stdin`.

## Claude Code

- Use the repository as a plugin/skill directory when launching Claude Code.
- Allow local `node` execution for `scripts/onepilot-agent.mjs`.
- Use `--agent-name "Claude Code"` when binding.
- Claude Code owns any local scheduler or reminder mechanism; OnePilot only returns structured recommendations.

## OpenClaw / ClawHub

- Install or publish the same OnePilot CLI package through OpenClaw/ClawHub as a Skill folder.
- Use `--agent-name OpenClaw` when binding.
- Keep OnePilot state in `~/.config/onepilot/agent.json`.
- If ClawHub requires scan/publish metadata, add only packaging metadata; do not fork CLI behavior.
- For first-stage distribution, publish the repository or release zip as a single OnePilot CLI package.
- The canonical package root is the directory containing `SKILL.md`; `scripts/` and `references/` must stay next to it.

## Gemini CLI

- Link or install the same skill folder with Gemini CLI skills commands.
- Use `--agent-name "Gemini CLI"` when binding.
- Gemini can load `SKILL.md`; local command permission still needs to allow Node execution.

## Qwen Code

- Qwen Code expects an extension package, so add a thin `qwen-extension.json` or extension wrapper when publishing there.
- The wrapper should call the same `scripts/onepilot-agent.mjs`; do not reimplement API calls.
- Use `--agent-name "Qwen Code"` when binding.
- The root `qwen-extension.json` points Qwen Code to `SKILL.md` and delegates commands to the shared CLI. If Qwen's registry later requires a stricter extension layout, keep this repository as the source package and generate the registry wrapper from it.

## opencode

- opencode expects an npm plugin. Publish a thin npm package only when needed.
- The plugin should expose commands that delegate to `scripts/onepilot-agent.mjs`.

## Trae And Other MCP-First Agents

- Prefer CLI execution today.
- When OnePilot MCP is available, use MCP for tools and keep this CLI as the compatibility fallback.

## WorkBuddy

- Treat WorkBuddy as experimental until the target WorkBuddy or SkillHub publishing flow confirms the required metadata.
- Prefer the OpenClaw/SkillHub-compatible package shape: a single folder containing `SKILL.md`, `scripts/`, `references/`, `README.md`, `LICENSE`, and `SECURITY.md`.
- If WorkBuddy installs Skills into `.codebuddy/skills/` or another managed directory, do not change shared commands; run them from the installed OnePilot CLI package root.
- If it can execute local commands, bind with `--agent-name WorkBuddy` and delegate to the shared CLI.
- If it exposes MCP but blocks local command execution, add a thin OnePilot MCP server later; do not rewrite recommendation, memory, subscription, feedback, or application behavior into WorkBuddy-specific code.
