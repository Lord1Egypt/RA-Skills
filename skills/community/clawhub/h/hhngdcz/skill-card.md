## Description:

Generates a complete `.claude` configuration structure for a project through guided prompts, including CLAUDE.md, settings, rules, and optional ClawHub skill installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhngdcz](https://clawhub.ai/user/hhngdcz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill in Claude Code to bootstrap project-level `.claude` configuration, permissions, rules, and documentation. It also supports optional selection or installation of skills from local Claude directories or ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies project-level Claude configuration, including permissions and rules.

Mitigation: Review generated or merged `.claude` files before relying on them, especially permissions.allow and permissions.deny.

Risk: The optional online flow can install unpinned third-party skills and the ClawHub CLI into an active agent environment.

Mitigation: Verify the ClawHub CLI source and version, inspect selected skills before installation, and prefer trusted or pinned releases where available.

Risk: The optional local-skills flow scans the user's local Claude skill inventory.

Mitigation: Use the local-skills flow only when that inventory may be reviewed for the current project, or skip it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hhngdcz/skills/hhngdcz)
- [Publisher profile](https://clawhub.ai/user/hhngdcz)
- [ClawHub CLI reference](reference/clawhub.md)
- [ClawHub skill browser](https://clawhub.ai/skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or merge project-level `.claude` files and optionally install selected skills.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact metadata reports 5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
