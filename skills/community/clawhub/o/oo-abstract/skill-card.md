## Description:

Validate an email address through Abstract Email Validation using the OOMOL-connected Abstract account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can check an email address's deliverability, quality, and risk signals through their connected Abstract account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may persistently install other agent instructions without this skill disclosing that behavior.

Mitigation: Review the CLI dependency before installation and use a reviewed release. If only Abstract access is needed, set OO_SKILLS_SYNC_DISABLED=1 before invoking oo.

Risk: Email addresses submitted for validation pass through OOMOL to Abstract.

Mitigation: Submit only addresses appropriate for validation through these services.

## Reference(s):

- [Abstract API documentation](https://docs.abstractapi.com/api)
- [Abstract](https://www.abstractapi.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [Shell commands with JSON input and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-action email validation results; no files generated.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
