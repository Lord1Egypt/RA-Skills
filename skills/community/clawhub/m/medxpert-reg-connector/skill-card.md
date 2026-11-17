## Description:

An MCP connector for medical device regulatory retrieval across MDR/CE, FDA 510(k), UDI, STED, classification, and global registration pathways, using a local read-only knowledge base covering 27 regulatory hubs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Regulatory affairs professionals and medical device teams use the connector to search reference material on classification, registration pathways, UDI, STED, and related requirements across China, the United States, Europe, Japan, and other markets. Confirm regulatory conclusions against current official sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regulatory material may be incomplete or out of date, and search results are not official determinations.

Mitigation: Verify requirements and conclusions against current official regulator sources.

Risk: A connected MCP host may handle query or result data according to its own policies, even when the connector runs locally.

Mitigation: Review the host's data handling and limit REG_HUB_REFS to documents approved for that environment.

Risk: An unpinned FastMCP dependency can change between installations.

Mitigation: Install a reviewed, pinned FastMCP version in an isolated environment.

Risk: The bundled attestation is not independent assurance and has a stale SKILL.md hash.

Mitigation: Refresh the attestation hash and obtain independent review before relying on it.

## Reference(s):

- [MedXpert regulatory knowledge hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/medxpert-reg-connector)
- [LGD formal paper](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured retrieval results with excerpts, source links, and brief guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search results from the bundled regulatory knowledge base; results are reference leads, not official regulatory determinations.]

## Skill Version(s):

1.0.3 (server-resolved release version; bundled SKILL.md states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
