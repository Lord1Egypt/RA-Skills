## Description:

Analyze federal government contracting data from SAM.gov, USAspending, and SBIR to profile contractors, find opportunities, and assess agency spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, GovCon analysts, and capture teams use this skill to connect an agent to Pipeworx GovCon Intel MCP for contractor profiles, opportunity scans, agency spending landscapes, award searches, and SBIR/STTR research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GovCon research may be sent to a third-party remote MCP service operated by Pipeworx.

Mitigation: Use only information you are comfortable sending to Pipeworx; avoid confidential bids, customer names, procurement strategy, controlled information, and personal data unless approved for that service.

Risk: The skill recommends remember/recall persistent memory tools without documented retention or deletion controls.

Mitigation: Avoid remember/recall for sensitive intermediate findings until retention, deletion, and user-control policies are understood.

## Reference(s):

- [Pipeworx Govcon Analyst ClawHub listing](https://clawhub.ai/brucegutman/skills/pipeworx-govcon-analyst)
- [SAM.gov](https://sam.gov/)
- [USAspending.gov](https://www.usaspending.gov/)
- [SBIR.gov](https://www.sbir.gov/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown text with MCP configuration JSON and structured research findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include contractor, opportunity, agency, award, spending, and SBIR/STTR findings returned through a third-party remote MCP service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
