## Description:

Use OSS Insight through the oo CLI to query GitHub repository activity, explore collections, and rank repositories by growth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to query OSS Insight for GitHub repository activity and trends, inspect repository collections, and rank collection repositories by issue, pull request, or star growth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs an online installer whose exact effects were not inspected.

Mitigation: Review and install a specific oo CLI release before enabling automatic setup; check account access, billing, and changes to other agents' skills. Set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: Collection ranking actions change OSS Insight state.

Mitigation: Keep the skill's approval requirement and confirm the exact payload and effect before running a write action.

## Reference(s):

- [OSS Insight](https://ossinsight.io)
- [OSS Insight API documentation](https://ossinsight.io/docs/api)
- [oo CLI documentation and controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON results and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by selected OSS Insight action.]

## Skill Version(s):

1.0.6 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
