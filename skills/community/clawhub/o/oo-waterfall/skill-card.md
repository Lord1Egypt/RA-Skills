## Description:

Use Waterfall through an OOMOL-connected account to read data, launch enrichment jobs, check job changes, and verify email addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read Waterfall account data, launch company or contact enrichment jobs, check job changes, and verify email addresses through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installer and changes to other agents’ skills were not available for inspection in this review.

Mitigation: Review and install a verified CLI release. Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if you do not want additional agent skills installed or refreshed.

Risk: Enrichment launch actions change Waterfall state, and the hosted service implementation was not established by this review.

Mitigation: Connect only the intended Waterfall account and review the exact write payload before running an enrichment launch action.

## Reference(s):

- [Waterfall API documentation](https://docs.waterfall.io/v1/authentication)
- [Waterfall](https://www.waterfall.io)
- [oo CLI documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [Waterfall ClawHub release](https://clawhub.ai/oomol/skills/oo-waterfall)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Connector action results as JSON, with shell commands and usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results vary by selected Waterfall operation.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
