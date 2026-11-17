## Description:

OpenClaw Skill Marketplace helps agents browse, search, recommend, synchronize, and install OpenClaw skills from ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwg2025](https://clawhub.ai/user/williamwg2025)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and skill maintainers use this skill to discover marketplace skills, compare recommendations by scenario, industry, or role, search local or synced ClawHub skill data, and install selected skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and sync flows run an unpinned npx clawhub command that can download or install third-party skills.

Mitigation: Use a pinned, trusted ClawHub CLI, inspect any skill before installation, and avoid running install or sync flows in sensitive workspaces without approval.

Risk: Marketplace operations can write synced skill data or installed skills under the user's OpenClaw skills directory.

Mitigation: Run the skill only where changes to the OpenClaw skills directory are expected, and keep backups or version control for local skill state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamwg2025/skills/openclaw-skill-marketplace)
- [README_EN.md](artifact/README_EN.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text, JSON configuration files, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Install and sync workflows can update the user's OpenClaw skills directory when explicitly run.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
