## Description:

Local credential vault with OS keychain integration, encrypted storage, and session-based access control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to define a local password-vault workflow with encrypted storage, OS credential-store sessions, confirmation rules, and safer credential delivery patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes local storage of credentials under ~/.vault and short-lived session tokens in the OS credential store.

Mitigation: Install only when that storage model matches the user's risk tolerance and keep confirmation enabled for sensitive entries.

Risk: Agent-readable credential access can expose sensitive accounts if confirmation policies are weakened.

Mitigation: Use the default low-sensitivity auto-access policy, require confirmation for medium through critical entries, and use a separate manager or vault for critical accounts when appropriate.

Risk: Password setup includes leak checks through a k-anonymity API.

Mitigation: Review whether that external check is acceptable for the deployment environment before setup.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown guidance with inline examples and operational rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Credentials must not be printed, logged, passed through command-line arguments, or exposed on domain mismatch or non-HTTPS requests.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
