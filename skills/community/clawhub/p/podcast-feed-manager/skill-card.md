## Description:

Manage personal podcast feeds through the fixed user-scoped huisheng.fm API from an installed skill package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quentinzhang](https://clawhub.ai/user/quentinzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to inspect and manage their user-scoped huisheng.fm podcast feeds and episodes from an agent sandbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a huisheng.fm Agent token that can read and modify podcast feeds.

Mitigation: Provide HUISHENG_API_TOKEN only in an isolated sandbox and avoid exposing command lines or logs to other local processes.

Risk: The CLI exposes update and delete operations without built-in confirmation.

Mitigation: Require explicit user confirmation before running update-feed, delete-feed, update-episode, or delete-episode commands.

## Reference(s):

- [huisheng.fm API Skill Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/quentinzhang/skills/podcast-feed-manager)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HUISHENG_API_TOKEN and curl; feed and episode operations are scoped to the authenticated user.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
