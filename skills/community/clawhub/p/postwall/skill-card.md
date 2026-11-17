## Description:

Secure email gateway for AI agents - human-in-the-loop approval for reading and sending emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperaiassist](https://clawhub.ai/user/casperaiassist)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use Postwall to let agents read only human-approved emails and submit outbound email drafts for human approval before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned external npm CLI that handles the PostWall API key and email data.

Mitigation: Install a pinned or otherwise verified PostWall CLI release, keep the API key scoped and rotatable, and review the package before use.

Risk: Polling can cause the agent to check for approved email during a session more often than intended.

Mitigation: Enable polling only when active email monitoring is needed and use an explicit polling cadence.

Risk: Reading an email marks it as read, which can hide it from later inbox or check commands.

Mitigation: Use inbox metadata and mark-read workflows deliberately, and read message bodies only when the agent is expected to consume them.

## Reference(s):

- [PostWall homepage](https://postwallapp.com)
- [PostWall repository](https://github.com/postwallapp/postwall)
- [ClawHub Postwall skill page](https://clawhub.ai/casperaiassist/skills/postwall)
- [ClawHub publisher profile](https://clawhub.ai/user/casperaiassist)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PostWall CLI commands can emit human-readable text or JSON with --json.]

## Skill Version(s):

1.7.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
