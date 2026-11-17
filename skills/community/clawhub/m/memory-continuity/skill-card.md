## Description:

Real Memory Continuity helps agents reflect after sessions, extract structured memories with confidence scores, and surface follow-up questions when the user returns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riley-coyote](https://clawhub.ai/user/riley-coyote)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add local continuity workflows that turn session activity into structured memory, identity notes, and follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist session-derived questions, identity notes, and reflection logs on local disk.

Mitigation: Use it only when local memory persistence is intended, avoid sensitive transcripts unless persistence is acceptable, and delete stored files manually when needed.

Risk: Heartbeat integration may trigger post-session reflection automatically after idle periods.

Mitigation: Enable the heartbeat workflow only when automatic post-session reflection is desired.

## Reference(s):

- [The Continuity Framework](references/framework.md)
- [ClawHub skill page](https://clawhub.ai/riley-coyote/skills/memory-continuity)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and local memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local questions, identity notes, and reflection logs under ~/clawd/memory or CONTINUITY_MEMORY_DIR.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
