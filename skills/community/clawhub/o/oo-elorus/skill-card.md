## Description:

Use this skill to read, create, and update Elorus data through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Elorus users use this skill to list and retrieve contacts, invoices, and products, or to create and update those records in their organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and add agent skills without clearly explaining those effects.

Mitigation: Install a verified oo CLI version, review its setup effects, and set OO_SKILLS_SYNC_DISABLED=1 if startup skill synchronization is not needed.

Risk: The remote installer and hosted connector implementation were not audited, and account permissions can expose Elorus records to actions.

Mitigation: Connect only the necessary Elorus account permissions and review invoice changes carefully.

## Reference(s):

- [Elorus](https://www.elorus.com/)
- [Elorus API documentation](https://developer.elorus.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action payloads and connector results, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read Elorus records or request changes; write actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
