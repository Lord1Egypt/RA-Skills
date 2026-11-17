## Description:

GigaMail gives an OpenClaw agent access to email, calendars, and Google Drive for reading, searching, drafting, and scheduling, with human approval required for destructive actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adecubed](https://clawhub.ai/user/adecubed)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use GigaMail to triage and search mail, draft replies, check calendar availability, and work with calendar or Drive items through an MCP server. A person approves destructive actions outside the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Drive and local spreadsheet access are not clearly disclosed for an email and calendar skill, and scan coverage is incomplete.

Mitigation: Review the missing source paths and confirm why Drive and spreadsheet access are needed; enable only the access required for the user's tasks.

Risk: Email content, sender details, and attachments may contain instructions that should not control the agent.

Mitigation: Treat message and attachment contents as data, and confirm with the user before taking requested actions.

## Reference(s):

- [GigaMail homepage](https://gigamail.ai)
- [GigaMail project repository](https://github.com/adecubed/gigamail)
- [GigaMail ClawHub release](https://clawhub.ai/adecubed/skills/gigamail)

## Skill Output:

**Output Type(s):** [Text, Guidance, API calls]

**Output Format:** [Text and structured MCP tool requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce email summaries, reply drafts, and calendar proposals. Destructive actions require out-of-band human approval.]

## Skill Version(s):

0.6.7 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
