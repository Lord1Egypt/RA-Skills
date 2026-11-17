## Description:

Lightweight experience-capture and behavior-hardening for Goat; it records high-value lessons from explicit feedback, promotes durable rules into memory when justified, and avoids verbose self-reflection loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevengaojn2010](https://clawhub.ai/user/stevengaojn2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use LessonLoop to capture important user corrections, preferences, repeated mistakes, and new operating rules as compact lessons. The skill helps agents apply feedback immediately while keeping long-term memory updates selective.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change persistent agent memory.

Mitigation: Review captured lessons before promotion and avoid storing secrets, temporary context, or sensitive material.

Risk: Scripts may write outside intended memory paths when invoked with unsafe arguments.

Mitigation: Restrict workspaces to approved directories and patch or wrap script execution so dates are validated and lesson content is bounded and sanitized.

## Reference(s):

- [Lesson types](references/lesson-types.md)
- [Ollama first-pass template](references/ollama-pass-template.md)
- [LessonLoop status/report format](references/status-format.md)
- [Publisher profile](https://clawhub.ai/user/stevengaojn2010)
- [ClawHub skill page](https://clawhub.ai/stevengaojn2010/skills/lessonloop)

## Skill Output:

**Output Type(s):** [guidance, markdown, JSON, shell commands]

**Output Format:** [Markdown guidance with optional JSON, JSONL logs, text reports, and shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes compact lessons to daily memory files and structured LessonLoop event logs when its scripts are invoked.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
