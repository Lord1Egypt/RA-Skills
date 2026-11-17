## Description:

Kaiqiao is a Chinese-language agent behavior calibration skill that guides an AI agent on when to ask clarifying questions, act without extra confirmation, push back, and give brief status feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leslietong2046-ship-it](https://clawhub.ai/user/leslietong2046-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use Kaiqiao to tune Chinese-language assistant behavior: ask when requirements are unclear, proceed on low-risk delegated tasks, raise objections with alternatives, and provide short progress or completion feedback. The skill also includes an optional local CLI helper for prompt checks and self-diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage inferred user traits or preferences to be written into shared long-term memory.

Mitigation: Require explicit user approval before any memory write and keep entries concise, reviewable, and removable.

Risk: The skill asks the agent to create recurring memory-scanning reminders.

Mitigation: Disable recurring reminders by default or require manual approval before creating and acting on them.

Risk: The skill's direct-action guidance could reduce confirmations for actions that should remain guarded.

Mitigation: Keep explicit confirmations for destructive, costly, public, financial, account-changing, or otherwise irreversible actions.

## Reference(s):

- [Kaiqiao ClawHub Skill Page](https://clawhub.ai/leslietong2046-ship-it/skills/kaiqiao-skill)
- [Behavior Checklist](references/checklist.md)
- [CLI Behavior Calibrator](references/kaiqiao.py)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with optional CLI commands and text diagnostic reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language behavioral guidance; optional local Python CLI uses standard library only]

## Skill Version(s):

2.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
