## Description:

Turn a plain-language task into a written AI agent loop: a loop brief with a checkable goal, a per-round process, evidence, a log, and stop conditions that an agent can run on its own. Use when the user asks for an AI agent loop or an agentic loop, says "make loop", "turn this into a loop", "keep iterating until it's good", or pastes a task with /make-loop. By default, only write the brief; do not start executing it in this session unless the user explicitly asks to run it now and confirms the scope. Domain knowledge comes from the current conversation and other skills, not from this one. Not a video or GIF loop tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ekko237](https://clawhub.ai/user/ekko237)

### License/Terms of Use:

MIT

## Use Case:

People using Claude Code, Codex, Cursor, or another supported AI agent can turn a plain-language task into a ready-to-copy loop brief with checkable goals, repeated steps, evidence, a log, and stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious because installation commands retrieve mutable remote content and scanners report a mismatch between the stated purpose and installation behavior.

Mitigation: Review the installation instructions and retrieved content before installing; use a reviewed exact CLI version and an immutable, reviewed repository revision.

## Reference(s):

- [Loop brief template](references/template.md)
- [Before-and-after examples](references/examples.md)
- [Delivery checklist](references/checklist.md)
- [Repository link documented by the skill](https://github.com/Ekko237/make-loop)
- [ClawHub skill listing](https://clawhub.ai/ekko237/skills/make-loop)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown loop brief in a code block, followed by a short summary of defaults and stop conditions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the brief by default; execution requires a clear request and confirmed scope.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
