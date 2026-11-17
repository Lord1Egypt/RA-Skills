## Description:

Apple Notary (developer.apple.com). Use this skill for ANY Apple Notary request — reading, creating, and updating data. Whenever a task involves Apple Notary, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check Apple Notary submission status and logs, list recent submissions, and reserve a new software submission through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may run downloaded software whose broader system changes are not explained.

Mitigation: Review or preinstall a pinned CLI, and check its skill installation and synchronization settings before enabling automatic setup.

Risk: Connecting Apple Notary grants OOMOL access to the connected account, and submission actions can change service state.

Mitigation: Keep approval of the exact submission payload enabled and inspect the live action schema before constructing it.

## Reference(s):

- [Apple Notary API documentation](https://developer.apple.com/documentation/notaryapi)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and service response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include temporary upload credentials or a time-limited download URL.]

## Skill Version(s):

1.0.4 (source: artifact frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
