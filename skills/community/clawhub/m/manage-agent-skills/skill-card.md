## Description:

Toggle skills across major coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunze7373](https://clawhub.ai/user/yunze7373)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to discover, audit, inspect, and manage the activation of installed skills across supported coding-agent platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing skill activation can affect which skills are available in a host.

Mitigation: Preview the selected host and every target before applying changes, and verify the result in the host after refreshing it.

Risk: Backups and inventory exports may contain secrets or private paths.

Mitigation: Keep backups and inventory exports private.

Risk: A failed batch may have partially changed settings, making an automatic retry unsafe.

Mitigation: Inspect current state before retrying a failed batch.

## Reference(s):

- [Manage Agent Skills release on ClawHub](https://clawhub.ai/yunze7373/skills/manage-agent-skills)
- [Codex skills guide](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills)
- [GitHub Copilot CLI configuration reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [Antigravity skills documentation](https://antigravity.google/docs/skills)
- [Gemini CLI skills documentation](https://geminicli.com/docs/cli/skills/)
- [OpenCode skills documentation](https://opencode.ai/docs/skills/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions, shell commands, and text or JSON CLI reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes preview and dry-run guidance; does not install skills or measure actual token savings.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
