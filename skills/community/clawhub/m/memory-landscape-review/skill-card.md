## Description:

Helps users review auto-memory, promote durable instructions into CLAUDE.md or local memory, and clean up duplicate or conflicting memory guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to audit project, local, and auto-memory layers, then decide what should be promoted, cleaned up, or left unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect repo memory, local memory, and auto-memory context that can contain personal or durable project instructions.

Mitigation: Install only if comfortable with that inspection scope, and review proposed memory changes before approval.

Risk: Incorrect promotion or cleanup could place stale, duplicate, or personal guidance into durable memory.

Mitigation: Use the skill's propose-first workflow and require explicit approval before any edits.

## Reference(s):

- [Memory Landscape Review Skill Page](https://clawhub.ai/wimi321/skills/memory-landscape-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with grouped recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports before edits; cleanup or promotion changes require explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
