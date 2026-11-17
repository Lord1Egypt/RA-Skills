## Description:

Operate Formspree through your OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to list and search Formspree form submissions through a connected account. It provides guidance for inspecting the action schema and handling connection setup when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs the agent to execute an unverified remote installer.

Mitigation: Review and approve the CLI installation separately, preferably using a pinned, verified release.

Risk: The connected workflow mediates access to Formspree submission data through OOMOL.

Mitigation: Connect only the intended Formspree account and consider how OOMOL should mediate access to submission data.

## Reference(s):

- [Formspree](https://formspree.io)
- [Form Submissions API documentation](https://help.formspree.io/articles/the-forms-api/form-submissions-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured submission data with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists submissions with optional filters; read-only action.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
