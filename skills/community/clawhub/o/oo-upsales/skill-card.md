## Description:

Use this skill to read, create, update, and delete Upsales data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and CRM users use the skill to look up companies, contacts, and users, and to create, update, or delete company and contact records in Upsales.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may introduce unreviewed code or changes to other agent skills, and the remote installers have not been verified.

Mitigation: Review and pin a specific CLI version before enabling the skill; consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: The hosted connector has not been verified and can access CRM data through the connected Upsales account.

Mitigation: Connect only the permissions needed for the task and retain approval for write and delete actions.

## Reference(s):

- [Upsales homepage](https://www.upsales.com/)
- [Upsales API documentation](https://api.upsales.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [CLI commands and JSON request/response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that create, update, or delete records require user confirmation.]

## Skill Version(s):

1.0.4 (source: artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
