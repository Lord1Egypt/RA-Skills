## Description:

Use the OOMOL-connected ValidEmail service to check email addresses and view remaining verification credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use it to verify email addresses and check remaining credits through their OOMOL-connected ValidEmail account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Startup skill synchronization may install or refresh additional agent skills.

Mitigation: Disable startup synchronization unless additional skills are intended to be installed or refreshed.

Risk: Uncapped retries may create paid verification attempts, and email addresses are shared through OOMOL with ValidEmail.

Mitigation: Set a maximum number of paid attempts and submit only addresses intended to be shared through OOMOL with ValidEmail.

Risk: The remote installers and deployed CLI binaries were not verified.

Mitigation: Review and install a verified CLI version before use.

## Reference(s):

- [ValidEmail](https://www.validemail.net/)
- [ValidEmail API response guide](https://www.validemail.net/Docs/response-guide)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification results or credit balance; each email verification consumes one credit.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
