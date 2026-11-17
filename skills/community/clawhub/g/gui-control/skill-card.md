## Description:

Control the GUI desktop on this machine using xdotool, scrot, and Firefox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vibes-me](https://clawhub.ai/user/vibes-me)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate a visible Linux desktop, open Firefox, capture screenshots, and interact with GUI applications through keyboard and mouse automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a live visible desktop, type text, submit forms, close applications, and capture screenshots.

Mitigation: Require explicit user confirmation before sensitive GUI actions such as typing, submitting forms, closing applications, or sharing screenshots.

Risk: Typed text and screenshots can expose passwords, tokens, private messages, banking details, or other sensitive information.

Mitigation: Avoid using the skill for credential entry, financial workflows, admin consoles, private communications, or other sensitive sessions.

Risk: Persistent memory guidance could cause future agents to reuse GUI behavior without enough user-control guardrails.

Mitigation: Review, remove, or constrain any persistent MEMORY.md guidance before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots through GUI tooling when the agent follows the skill workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
