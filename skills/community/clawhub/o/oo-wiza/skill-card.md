## Description:

Wiza (wiza.co). Use this skill for ANY Wiza request — reading, creating, and updating data. Whenever a task involves Wiza, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a connected Wiza account use this skill to check credits, search prospects, retrieve list and reveal results, and start an individual contact reveal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to run a remote installer whose behavior is unverified.

Mitigation: Review setup behavior, install a verified CLI release yourself, require approval before any remote installer runs, and check whether the CLI installs or synchronizes additional agent skills.

Risk: Starting an individual reveal changes Wiza state.

Mitigation: Confirm the exact action and payload with the user before running it.

## Reference(s):

- [Wiza API documentation](https://docs.wiza.co/)
- [Wiza](https://wiza.co)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses with task-oriented text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Wiza data; starting an individual reveal is a write action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
