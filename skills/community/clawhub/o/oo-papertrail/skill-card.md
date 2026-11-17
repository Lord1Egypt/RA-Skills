## Description:

Operate Papertrail to search event logs and manage saved searches through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Papertrail account users use this skill to search event logs, inspect groups, systems, and saved searches, and manage saved searches through the oo CLI. It requires approval before creating, replacing, or deleting saved searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup uses an unverified remote installer, and the hosted connector implementation is unverified.

Mitigation: Install a reviewed oo CLI version yourself and confirm that OOMOL may process your Papertrail data.

Risk: Setup may make broader changes to installed agent skills that the setup guidance does not explain.

Mitigation: Consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI.

Risk: Creating, replacing, or deleting a saved search changes or removes Papertrail data.

Mitigation: Keep the skill's approval requirements and confirm the target and effect before running these actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Papertrail HTTP API documentation](https://www.papertrail.com/help/http-api/)
- [Papertrail](https://www.papertrail.com)
- [OOMOL skill synchronization control](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow live connector schemas; user approval is required for saved-search writes and deletions.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
