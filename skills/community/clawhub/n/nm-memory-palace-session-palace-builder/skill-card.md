## Description:

Builds session-scoped temporary memory palaces for extended conversations

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other knowledge workers use the skill to organize temporary project or conversation state, including decisions, artifacts, issues, and next steps, and recover that context after interruptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session palaces may contain sensitive conversation details, code, requirements, or research that could be retained in exported or archived state.

Mitigation: Keep credentials and private data out of session state, and review palace contents before exporting or archiving them.

## Reference(s):

- [Session palace templates](modules/templates.md)
- [Skill homepage (metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-memory-palace-session-palace-builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured text or Markdown organized into named rooms and project-state sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session-scoped organization for decisions, progress, issues, artifacts, and next steps, with checkpoint guidance.]

## Skill Version(s):

1.10.3 (source: frontmatter; ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
