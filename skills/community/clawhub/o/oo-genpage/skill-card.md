## Description:

GenPage (genpage.ai). Use this skill for ANY GenPage request — reading, creating, updating, and deleting data. Whenever a task involves GenPage, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read GenPage workspace data and manage audiences and campaigns through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified OO CLI downloads.

Mitigation: Verify the CLI release before installing or allowing automatic setup.

Risk: Startup may introduce persistent agent skills beyond this integration.

Mitigation: Decide whether automatic skill synchronization is acceptable; set OO_SKILLS_SYNC_DISABLED=1 to suppress startup skill writes.

Risk: GenPage changes can affect workspace data.

Mitigation: Use limited GenPage permissions and retain approval for writes and destructive changes.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [GenPage](https://www.genpage.ai/)
- [GenPage API documentation](https://backend.genpage.ai/docs/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [GenPage connector results as JSON with natural-language summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include reads, writes, and destructive operations; writes require confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
