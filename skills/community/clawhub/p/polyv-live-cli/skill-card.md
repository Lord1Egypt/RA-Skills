## Description:

This skill helps agents use the npm-published polyv-live-cli to manage PolyV Cloud Live services, including channels, streams, playback, interactions, viewers, access controls, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyv](https://clawhub.ai/user/polyv)

### License/Terms of Use:

MIT-0

## Use Case:

External PolyV operators, support teams, and developers use this skill to query and administer live-streaming channels and related resources through the current npm CLI. It supports operational workflows such as account setup, channel and stream management, interaction tools, playback, viewer controls, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a mutable npm latest package for live administrative operations.

Mitigation: Prefer a pinned, reviewed polyv-live-cli version before production use and re-check help output before executing command families.

Risk: The skill can access PolyV administrative credentials and perform high-impact account actions.

Mitigation: Use least-privilege PolyV credentials, verify the active account before writes, and avoid exposing AppSecret or other credentials in logs or responses.

Risk: Write, delete, bulk, force, push, start, stop, merge, transcode, and similar commands can affect production live-streaming resources.

Mitigation: Confirm target channels or objects before execution, avoid --force unless separately authorized, and test against temporary resources when practical.

Risk: Stream keys and full RTMP URLs are sensitive operational secrets.

Mitigation: Return full stream credentials only when explicitly requested for trusted streaming endpoints and keep them out of public channels and persistent logs.

## Reference(s):

- [PolyV official site](https://www.polyv.net/)
- [PolyV Live API documentation](https://help.polyv.net/#/live/api/)
- [Skill instructions](SKILL.md)
- [Task routing](references/task-routing.md)
- [Command index](references/command-index.md)
- [Authentication configuration](references/authentication.md)
- [Streaming operations](references/streaming.md)
- [Channel management](references/channel-management.md)
- [Chat management](references/chat-management.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PolyV CLI commands that require configured credentials; data extraction workflows prefer JSON output.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
