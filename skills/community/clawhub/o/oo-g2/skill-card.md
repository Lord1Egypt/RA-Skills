## Description:

Use a connected G2 account to read, create, update, or delete G2 data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to query G2 data and manage products, reviews, research boards, reports, and buyer intent through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified downloaded software without asking and introduce broader persistent agent changes.

Mitigation: Review setup first, install a reviewed and pinned CLI release yourself, and check its automatic skill-installation behavior.

Risk: Connecting G2 entrusts OOMOL with account access; actions may post data, spend credits, or delete data.

Mitigation: Grant only needed permissions and retain confirmation for posting, spending credits, and deletion.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [G2](https://www.g2.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected G2 action and the connected account's permissions and entitlements.]

## Skill Version(s):

1.0.2 (source: evidence metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
