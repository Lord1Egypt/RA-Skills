## Description:

Maintain the canonical live OpenClaw main checkout, macOS LaunchAgent-managed Gateway, local macOS app, exact-head main CI, and recurring full release validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to fast-forward an operator-selected macOS OpenClaw checkout, verify its managed Gateway and app, inspect exact-head CI, and run non-publishing release validation. It guides focused repairs through the controlling worktree and PR workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the skill suspicious for review, and unresolved local path references leave some targets unassessed.

Mitigation: Review the skill and inspect the referenced local files before installing; the available scan is incomplete and does not establish that the skill creates persistence or is malicious.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hillstreet-ph/skills/oc-live-updater)
- [OpenClaw issue 114967](https://github.com/openclaw/openclaw/issues/114967)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, JSON]

**Output Format:** [Markdown guidance, shell commands, and JSON status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
