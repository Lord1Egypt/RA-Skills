## Description:

Enables peer-to-peer cross-communication between isolated OpenClaw agents so they can send asynchronous messages across agent boundaries with multiline support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxue1985122219](https://clawhub.ai/user/zhangxue1985122219)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let isolated local OpenClaw agents send asynchronous peer-to-peer messages and wake each other for coordination. First-time setup generates a protocol block that a user manually installs in each target agent's AGENTS.md file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install persistent rules that make agents act on unauthenticated background messages.

Mitigation: Install only in trusted local agent groups, treat intercom messages as untrusted input, restrict allowed senders and targets, and require human approval for consequential actions.

Risk: Background cross-agent messaging can make replies and follow-on actions less visible to the user.

Mitigation: Keep intercom replies visible or logged, and avoid pasting the generated protocol into broad or privileged agents without additional local rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangxue1985122219/skills/multi-agent-intercom)
- [Package repository](https://github.com/openclaw/multi-agent-intercom.git)
- [Package issue tracker](https://github.com/openclaw/multi-agent-intercom/issues)
- [Package homepage](https://clawhub.com/skills/multi-agent-intercom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup prints a protocol block for manual installation; send commands return immediately after launching a background OpenClaw agent message.]

## Skill Version(s):

1.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
