## Description:

Find, audit and manage installed agent skills across eight hosts. Use to locate missing or disabled skills, diagnose duplicate or outdated manager copies, and change skill visibility on request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunze7373](https://clawhub.ai/user/yunze7373)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Codex, Claude Code, GitHub Copilot CLI, OpenClaw, Hermes, Antigravity, Gemini CLI, or OpenCode use this skill to find, audit, and manage skill visibility on a selected host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes platform-management features that use environment, file, and shell capabilities.

Mitigation: Check that these capabilities fit the target environment, inspect the exact target, and preview mutations with --dry-run before proceeding.

Risk: The security review reports that one referenced guide was only partly analyzed.

Mitigation: Review the relevant guide directly before relying on its instructions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yunze7373/skills/manage-agent-skills)
- [Codex skills guide](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [GitHub Copilot CLI configuration](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-config-dir-reference)
- [OpenClaw skills](https://docs.openclaw.ai/tools/skills)
- [Hermes skill utilities](https://github.com/NousResearch/hermes-agent/blob/main/agent/skill_utils.py)
- [Antigravity skills](https://antigravity.google/docs/skills)
- [Gemini CLI skills](https://geminicli.com/docs/cli/skills/)
- [OpenCode skills](https://opencode.ai/docs/skills/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration files, Reports]

**Output Format:** [Markdown guidance and text or JSON reports, with configuration changes when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations are scoped to a selected host platform and skill target.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
