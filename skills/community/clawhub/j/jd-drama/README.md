# JianDan Short-Drama Skill

Official Agent Skill for the JianDan AI marketing short-drama platform. It teaches Codex, OpenClaw, TRAE, and other compatible agents how to operate short-drama projects safely through the `jd-drama` CLI.

[中文说明](./README.zh-CN.md)

## Status

- Skill version: `1.0.0-beta.6`
- CLI package: `@flyengine/jd-drama-cli`
- Service: [jiandan.flyengine.cn](https://jiandan.flyengine.cn/)
- Stage: public beta

The public beta connects to production user data and real quotas. All write operations must be previewed with `--dry-run` and explicitly approved with `--confirm`.

## Capabilities

- Discover and inspect short-drama projects, brands, and material libraries.
- Create projects from an AI idea or an uploaded script.
- Read, replace, verify, version, and restore official script episodes.
- Extract and parse assets through the system for uploaded, AI-generated, and secondary-created scripts; edit and regenerate existing parsed assets.
- Generate, inspect, optimize, and update storyboard segments, including Seedance 2.5 configuration.
- Generate and inspect video tasks; attach a local video to a storyboard segment.
- Diagnose failed tasks and produce recovery plans.

## Install

Install the CLI first:

```bash
npm install -g @flyengine/jd-drama-cli@beta
jd-drama --version
```

Install the bundled skill for your agent:

```bash
# Codex
jd-drama --json skill install --target codex --scope user --dry-run
jd-drama --json skill install --target codex --scope user --confirm

# OpenClaw
jd-drama --json skill install --target openclaw --scope user --dry-run
jd-drama --json skill install --target openclaw --scope user --confirm

# TRAE, run in the target project
jd-drama --json skill install --target trae --scope project --project-dir . --dry-run
jd-drama --json skill install --target trae --scope project --project-dir . --confirm

# WorkBuddy, run in the target project and follow the returned harness sync steps
jd-drama --json skill doctor --target workbuddy
```

The same `SKILL.md` can also be installed directly from this repository using the target agent's GitHub skill installation workflow.

## Authorize

```bash
jd-drama auth login
jd-drama --json release-check
```

Authorization happens in the JianDan website. Never provide a JianDan password or manually copied token to an agent.

Local agents normally share one browser authorization. Check `jd-drama --json doctor` and authorize only when `auth.browserAuthorization.needsLogin` is true. Do not log out and log in as an automatic repair: logout revokes the shared session for all tools. Resolve filesystem, Keychain, or network diagnostics before retrying. Missing brand/material scopes require one new browser approval, without a preceding logout.

## Quick Start

```bash
jd-drama --json projects list --limit 10
jd-drama --json brands list --limit 10
jd-drama --json materials folders
jd-drama --json ai-script options
jd-drama --json tasks recovery-plan PROJECT_ID
```

Preview project creation without writing data:

```bash
jd-drama --json ai-script create \
  --idea "A fast-paced urban product marketing short drama" \
  --episode-count 1 \
  --name "Agent beta test" \
  --generate \
  --dry-run
```

## Safety

- Use `--json` for agent calls.
- Run the exact command with `--dry-run` before replacing it with `--confirm`.
- Do not bypass CLI safety boundaries through raw API calls.
- Do not expose passwords, authorization codes, local configuration files, or tokens.
- Do not test destructive commands against valuable production projects.
- Brand association is available only during initial project creation.
- Asset records must be created by system extraction and parsing, never manually or through direct API calls. Wait for extraction to succeed before deep parsing, and for parsing to succeed before image generation. Deep parsing may consume credits.
- Upgrade every local CLI/MCP client. The matching backend update blocks manual creation from older clients only after that backend is deployed.

Read [SKILL.md](./SKILL.md) for the full agent workflow.

## License

The Skill files in this repository are released under the [MIT-0 License](./LICENSE). This license does not cover the JianDan service, API, CLI implementation, trademarks, user accounts, quotas, or generated content. See [NOTICE](./NOTICE).
