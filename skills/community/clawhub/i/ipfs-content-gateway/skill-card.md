## Description:

Guides agents to retrieve IPFS content by CID, upload and pin files up to 10 MB, and list prior uploads through AgentPMT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve content by IPFS CID, upload and pin files, and review upload history through AgentPMT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pinned IPFS content may remain accessible after upload.

Mitigation: Do not upload secrets, credentials, regulated data, or confidential files unless intentionally encrypted first.

Risk: CIDs, gateway links, and filenames may reveal sensitive context.

Mitigation: Choose non-sensitive filenames and share CIDs and gateway links only when their exposure is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/agentpmt/skills/ipfs-content-gateway)
- [AgentPMT IPFS Content Gateway](https://www.agentpmt.com/marketplace/ipfs-content-gateway)
- [AgentPMT account and MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Guidance, Text, JSON]

**Output Format:** [Markdown instructions and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieval returns a text preview or binary indicator with content metadata; uploads return a CID and gateway links; listing returns upload history.]

## Skill Version(s):

1.0.1 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
