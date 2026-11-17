## Description:

Guided meditation with breathing exercises and session tracking. Use when practicing mindfulness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to provide guided breathing, meditation prompts, simple timers, and local session tracking for mindfulness practice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bash timer can run unintended shell commands from a crafted timer argument.

Mitigation: Validate timer input as a simple bounded integer before using it, and avoid untrusted or generated timer arguments until the script is fixed.

Risk: Meditation session history is stored locally.

Mitigation: Treat local session records as personal data and review, restrict, or delete ~/.local/share/meditation-guide/ as appropriate.

Risk: Intense breathing exercises may be unsuitable for some users.

Mitigation: Use caution with intense breathing patterns and apply appropriate medical judgment for users with relevant conditions.

## Reference(s):

- [Meditation Guide on ClawHub](https://clawhub.ai/bytesagain3/skills/meditation-guide)
- [bytesagain3 publisher profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance, Files]

**Output Format:** [Terminal text, Markdown command examples, and local JSONL session records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores meditation session history locally under ~/.local/share/meditation-guide/.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
