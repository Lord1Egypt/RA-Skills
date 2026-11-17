## Description:

Search Findymail for professional contact data, verify email addresses, and check credit usage through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers can find professional email addresses by name and company domain, search company employees, verify addresses, and check Findymail credit usage through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes downloaded code whose exact effects have not been verified.

Mitigation: Review setup first, install a verified fixed-version CLI yourself, require approval for installation changes, and review or disable automatic skill synchronization.

Risk: Using the connected Findymail integration involves OOMOL handling the integration and its credentials server-side.

Mitigation: Connect Findymail only if you accept OOMOL handling the integration.

## Reference(s):

- [Findymail homepage](https://www.findymail.com/)
- [Findymail API documentation](https://app.findymail.com/docs/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis]

**Output Format:** [Findymail connector results as JSON, with natural-language findings when summarized by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results, email verification results, and credit usage information]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
