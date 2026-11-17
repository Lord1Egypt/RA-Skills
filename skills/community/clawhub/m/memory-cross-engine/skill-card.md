## Description:

memory-cross-engine provides a local structured memory bus so planner, memory, verification, and reflection agents can write, link, retrieve, and inspect shared task memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to share structured memory across planning, memory, verification, and reflection components during long-running tasks. It supports cross-engine retrieval, explicit entry linking, per-engine filtering, and a global memory view.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist free-form task content, notes, failures, and preferences across sessions.

Mitigation: Do not store secrets or sensitive work data in the memory files; review stored entries before reuse or sharing.

Risk: The learning workflow encourages agents to reuse stored preferences and may write learned experience back into skill instructions.

Mitigation: Require human review before automatically applying stored preferences or modifying SKILL.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/memory-cross-engine)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-backed local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and retrieves local JSONL memory entries and learned preference records when its scripts are used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
