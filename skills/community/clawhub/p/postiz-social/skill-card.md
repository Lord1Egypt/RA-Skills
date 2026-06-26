## Description: <br>
Manage social publishing, scheduled posts, and content workflows in Postiz via the Postiz API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, social media operators, and developers use this skill to inspect Postiz workspaces and posts, schedule new content, review publishing queues, and manage social publishing workflows through ClawLink-backed Postiz tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawLink brokers access to the user's connected Postiz account and handles sensitive account credentials. <br>
Mitigation: Install only if the user trusts ClawLink, and have the user review the account connection prompt before connecting Postiz. <br>
Risk: Publishing, editing, scheduling, or deleting posts can affect live social accounts. <br>
Mitigation: Preview and confirm the target resource, content, schedule, and intended effect before any write or destructive action. <br>


## Reference(s): <br>
- [Postiz](https://postiz.com/) <br>
- [Postiz API Documentation](https://docs.postiz.com/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [Postiz Social Publishing on ClawHub](https://clawhub.ai/hith3sh/postiz-social) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Postiz account through ClawLink; write actions require explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
