## Description:

Use when Hermes web tools fail or need configuring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose Hermes web_search and web_extract backend selection, configuration, provider availability, and site-specific extraction failures before choosing a fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The troubleshooting flow may reveal local Hermes configuration details or the names of configured web-provider API key variables.

Mitigation: Inspect only provider names and configuration selections needed for diagnosis, do not expose secret values, and make no configuration changes unless the user explicitly approves a fix.

Risk: Incorrectly treating a site-specific extraction failure as a global tool failure can lead to unnecessary configuration changes.

Mitigation: Run a differential test against a known-good URL first, then present findings and fix options before taking action.

## Reference(s):

- [Web Backend Selection Internals](references/backend-selection-internals.md)
- [Project homepage](https://github.com/mina-atef-00/agent-skills)
- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/hermes-web-tools)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic guidance that presents fix options and waits for explicit user approval before configuration changes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
