## Description:

PollyReach gives every AI agent a phone number and the ability to get things done over the phone, including finding contacts, making calls, and completing tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pollyreach](https://clawhub.ai/user/pollyreach)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use PollyReach to make outbound phone calls, manage incoming call summaries, update answering behavior, and check activation or account balance through PollyReach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Call instructions, caller information, transcripts, and recording links may be processed by PollyReach.

Mitigation: Use the skill only with user consent for third-party processing, and keep shared call details limited to what the task requires.

Risk: Outbound calls and scheduled inbound-call polling can affect people outside the agent session.

Mitigation: Require explicit user confirmation before placing calls or enabling recurring polling.

Risk: Broad activation, full transcript disclosure, and promotional account messages can expose more information than necessary.

Mitigation: Avoid publicizing the assigned number or full transcripts unless necessary, and omit promotional account content unless it is directly relevant.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pollyreach/skills/pollyreach)
- [PollyReach Homepage](https://pollyreach.ai)
- [PollyReach Publisher Profile](https://clawhub.ai/user/pollyreach)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell-command invocations and JSON or text command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include call summaries, transcripts, balance status, activation status, and recording or detail links returned by PollyReach.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
