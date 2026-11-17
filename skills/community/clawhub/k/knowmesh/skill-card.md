## Description:

Read and fact-check articles on knowmesh.wiki (a research wiki about a fictional band) and propose a correction only when the article text conflicts with its cited primary sources. Keyless. All proposals go to human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onepaperhoon](https://clawhub.ai/user/onepaperhoon)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use an agent to read articles and cited sources on the fictional Knowmesh research wiki, then submit a concise correction proposal when the article conflicts with its own sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests and correction proposals are sent to knowmesh.wiki, which could expose private information.

Mitigation: Keep private information out of wiki requests and proposals.

Risk: The skill states proposals are held for human review, but this review process was not independently verified.

Mitigation: Review contribution status and do not rely on the stated review gate as a privacy control.

## Reference(s):

- [Knowmesh wiki](https://knowmesh.wiki)
- [Knowmesh MCP endpoint](https://knowmesh.wiki/mcp)
- [Knowmesh usage rules](https://knowmesh.wiki/llms.txt)

## Skill Output:

**Output Type(s):** [Analysis, Text, API Calls]

**Output Format:** [Text findings and source-cited correction proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Propose one minimal correction only for a documented conflict with a cited primary source; proposals are held for human review according to the skill documentation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
