## Description:

Use ByteForms to search for and read forms and response data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to find ByteForms forms, retrieve a form, and read its responses through an account connected to OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a remote installer that has not been verified.

Mitigation: Review the installer and use a separately reviewed, pinned oo CLI installation.

Risk: The required CLI can silently install or refresh other agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if other skills should not be installed or refreshed.

Risk: Form responses may pass through OOMOL when using the connected account.

Mitigation: Connect only the intended ByteForms account and consider whether its response data may pass through OOMOL.

## Reference(s):

- [ByteForms](https://forms.bytesuite.io/)
- [ByteForms API documentation](https://dev.forms.bytesuite.io/docs/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses and concise usage guidance, with shell commands for the oo CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns form and response data for the connected ByteForms account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
