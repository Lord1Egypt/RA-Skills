## Description:

Use Faktoora through an OOMOL-connected account to read, create, update, or delete projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to access Faktoora project data and manage projects through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded code that has not been verified.

Mitigation: Review the installer before allowing setup and use an independently verified, fixed release.

Risk: OOMOL mediates access to the connected Faktoora account, and agent skill synchronization may occur automatically.

Mitigation: Review the connection and synchronization behavior; use OO_SKILLS_SYNC_DISABLED when synchronization should be disabled.

Risk: Project changes and deletion can affect Faktoora data.

Mitigation: Keep the skill's confirmation requirements for the exact change or deletion target.

## Reference(s):

- [Faktoora API documentation](https://docs.faktoora.com/)
- [Faktoora](https://faktoora.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Faktoora ClawHub release](https://clawhub.ai/oomol/skills/oo-faktoora)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include Faktoora data and execution metadata.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
