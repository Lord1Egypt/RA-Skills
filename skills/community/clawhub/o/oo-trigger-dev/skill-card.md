## Description:

Trigger.dev (trigger.dev). Use this skill for ANY Trigger.dev request — reading, creating, updating, and deleting data. Whenever a task involves Trigger.dev, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Trigger.dev runs and retrieve results, trigger or replay tasks, and cancel runs through an OOMOL-connected account. Writes and cancellations require user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can run an unverified remote installer without separate user approval; the remote installer payload was unavailable for inspection.

Mitigation: Review and approve CLI installation separately, preferably using a verified, fixed release. Check automatic skill-synchronization settings before use.

Risk: OOMOL is part of the credential and request trust boundary for connected Trigger.dev actions.

Mitigation: Review the connection and request handling, and preserve the skill's confirmation requirements for changes and cancellations.

## Reference(s):

- [Trigger.dev](https://trigger.dev)
- [Trigger.dev management API authentication](https://trigger.dev/docs/management/authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON results with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the connected Trigger.dev account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
