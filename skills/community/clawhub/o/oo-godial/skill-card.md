## Description:

Operate GoDial through an OOMOL-connected account to retrieve account, list, and contact data or create contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with the oo CLI and a connected GoDial account can retrieve accounts, lists, and contacts, or create a contact after reviewing the exact payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The oo CLI's startup skill synchronization can install agent skills beyond this GoDial workflow.

Mitigation: Review and install a fixed CLI release; consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking oo.

Risk: A contact creation action changes GoDial data, and the connected account or submitted fields may be unintended.

Mitigation: Confirm the connected GoDial account and review the exact write payload before running the action.

Risk: The external CLI installer and hosted connector implementation have not been verified.

Mitigation: Use a fixed CLI release from a trusted source and verify it before enabling the skill.

## Reference(s):

- [GoDial on ClawHub](https://clawhub.ai/oomol/skills/oo-godial)
- [GoDial API integration guide](https://godial.cc/blog/integrating-your-website-or-crm-with-godial-using-api/)
- [GoDial homepage](https://godial.cc)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON action payloads and text responses invoked through shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
