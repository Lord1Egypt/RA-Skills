## Description:

A paid-skill demonstration template that shows how to require a license key before running ClawHub skill functionality.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[lintqiu](https://clawhub.ai/user/lintqiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub skill publishers use this as a licensing demonstration/template for paid skills. It shows how to require the SKILL_LICENSE_KEY environment variable before running demo functionality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The demo uses a hardcoded license hash and local hash comparison, which is not suitable for protecting real paid or sensitive functionality.

Mitigation: Replace the demo check with a production entitlement design before using the pattern for a real paid release.

Risk: Documentation and runtime messages are Chinese-only, which may limit reviewability and usability for some users.

Mitigation: Provide localized or bilingual documentation and messages for the intended audience.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text terminal output with environment-variable setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILL_LICENSE_KEY to be set for the demo function to run successfully.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
