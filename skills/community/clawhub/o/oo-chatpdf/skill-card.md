## Description:

ChatPDF (chatpdf.com). Use this skill for ANY ChatPDF request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to import publicly reachable PDFs into ChatPDF, ask questions about imported sources, and manage sources through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can automatically execute a remote installer that was unavailable for inspection.

Mitigation: Review and install a verified CLI release yourself before running the skill, and check any bundled agent-skill changes.

Risk: The skill operates through the connected ChatPDF account, including importing sources and deleting selected sources.

Mitigation: Confirm intended imports and deletion targets before running state-changing actions.

## Reference(s):

- [ChatPDF skill release](https://clawhub.ai/oomol/skills/oo-chatpdf)
- [ChatPDF](https://www.chatpdf.com)
- [ChatPDF API documentation](https://www.chatpdf.com/docs/api/backend)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON action responses and text answers; shell command syntax for actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can import or delete ChatPDF sources; the skill documents approval requirements for state-changing actions.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
