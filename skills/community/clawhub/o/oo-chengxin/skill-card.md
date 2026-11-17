## Description:

Search and read Tongcheng Chengxin travel information through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and agents can search Tongcheng Chengxin for flights, trains, buses, hotels, attractions, transport, and travel products. The skill returns search information through the connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes remote code, and its exact changes were unavailable for review.

Mitigation: Review and verify the CLI release before installation; set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: Searches use the connected account and may consume credit.

Mitigation: Check the applicable account and billing limits before running searches.

## Reference(s):

- [Tongcheng Chengxin homepage](https://www.ly.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-chengxin)

## Skill Output:

**Output Type(s):** [JSON data, Travel information]

**Output Format:** [Structured search results with travel details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on the connected account and provider availability.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
