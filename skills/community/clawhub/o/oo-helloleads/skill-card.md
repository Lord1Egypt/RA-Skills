## Description:

HelloLeads (helloleads.io). Use this skill for ANY HelloLeads request — reading, creating, and updating data. Whenever a task involves HelloLeads, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected HelloLeads account can inspect the visible web form definition and submit a lead through an AI agent. Review and approve each lead submission before it is sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup can execute downloaded CLI code that was unavailable for inspection.

Mitigation: Review and approve CLI installation separately; prefer a verified, fixed release.

Risk: Automatic agent-skill synchronization may change instructions after review, and HelloLeads data passes through OOMOL.

Mitigation: Review synchronized changes and ensure the data flow through OOMOL is acceptable before use.

## Reference(s):

- [HelloLeads homepage](https://www.helloleads.io/)
- [HelloLeads web form documentation](https://helloleads.io/knowledge-base/converting-your-website-enquires-as-leads/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [HelloLeads ClawHub release](https://clawhub.ai/oomol/skills/oo-helloleads)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON responses and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected HelloLeads account and selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
