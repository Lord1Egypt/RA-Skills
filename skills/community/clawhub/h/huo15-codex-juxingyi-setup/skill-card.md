## Description:

Installs or checks Codex desktop and CLI, configures Codex to use the Juxingyi gateway, and exposes Codex status and session context to an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to set up Codex with a third-party Juxingyi model gateway and inspect Codex installation, configuration, project, and session context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The context and session scripts can expose Codex configuration, prior prompts, code, file paths, tool outputs, or secrets.

Mitigation: Review scripts before execution, run them manually rather than in automation, and prefer a test CODEX_HOME or sanitized Codex configuration.

Risk: The configuration script writes Codex provider settings and uses a Juxingyi API key.

Mitigation: Use a dedicated or least-privilege API key, confirm the gateway endpoint, and review the backed-up and updated config.toml after running.

Risk: The skill calls a third-party model gateway when retrieving models or checking connectivity.

Mitigation: Only run it on networks and projects where routing Codex traffic through the configured gateway is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-codex-juxingyi-setup)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)
- [Juxingyi console](https://fireworks-simulator.huo15.com/app/)
- [Juxingyi API base](https://fireworks-simulator-api.huo15.com/v1)
- [ChatGPT download](https://chatgpt.com/download)
- [Homebrew](https://brew.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and TOML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read Codex configuration and session files, and may call the configured model gateway when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
