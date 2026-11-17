## Description:

Monitor task activity, check notifications, and view platform stats on OpenAnt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check OpenAnt notifications, monitor task status, inspect escrow and wallet state, watch tasks, and view platform statistics through the OpenAnt CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned remote OpenAnt CLI in an authenticated account.

Mitigation: Install only after accepting that account access, and prefer a release that pins the CLI package.

Risk: The skill can change notification or account state, including marking notifications read and creating task subscriptions.

Mitigation: Prefer narrower command permissions and require confirmation before state-changing notification or watch actions.

Risk: Wallet and notification permissions are broad for a monitoring workflow.

Mitigation: Limit permissions to exact commands needed for monitoring before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown with inline bash code blocks and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to append --json for structured OpenAnt CLI output.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
