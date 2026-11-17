## Description:

Search Tonghuashun Financial Data and retrieve A-share market, company, fund, and index information through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search Tonghuashun instruments and retrieve A-share market, company financial, public fund, and index data through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time CLI installer and its automatic skill synchronization are unverified.

Mitigation: Review and approve the CLI installation separately before running it.

Risk: Export actions upload market datasets to transit storage without an explicit confirmation rule in the skill.

Mitigation: Require confirmation before each export, and clarify the storage destination and retention before uploading.

## Reference(s):

- [Tonghuashun Financial Data API Documentation](https://fuyao.aicubes.cn/docs/)
- [Tonghuashun Financial Data](https://fuyao.aicubes.cn/)
- [oo CLI Repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured connector results in JSON with concise text summaries as requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available fields vary by action; consult the action schema before making a request.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
