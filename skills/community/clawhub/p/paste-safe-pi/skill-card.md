## Description:

Emits short, pure-ASCII shell commands and read-back checks that survive hand-pasting into remote terminals that garble non-ASCII input or mangle multi-line pastes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharinchan233](https://clawhub.ai/user/sharinchan233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when advising users who hand-paste commands into unreliable SSH or Raspberry Pi terminals. It helps produce safe one-line sed edits, append commands, and verification read-backs instead of heredocs or fragile multi-line blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated sed, echo, or shell commands can modify files on the target machine if pasted without review.

Mitigation: Review each generated command before pasting it, and use the paired read-back command to confirm the intended change.

Risk: The skill is specialized for unreliable hand-paste remote shells and may be unnecessary when direct file writing or script execution is available.

Mitigation: Use direct file-writing tools or a script file when the environment supports them cleanly.

## Reference(s):

- [Worked Examples](reference.md)
- [ClawHub Skill Page](https://clawhub.ai/sharinchan233/skills/paste-safe-pi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with short single-line shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure ASCII commands; file-editing commands are paired with read-back verification when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
