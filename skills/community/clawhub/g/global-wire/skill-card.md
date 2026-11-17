## Description:

Turn answers about major world events into wire-style briefings, rolling event timelines, verification notes, and alert bullets with stable formatting, source priority, and confidence labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yly46967-source](https://clawhub.ai/user/yly46967-source)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use GlobalWire to convert major world-news answers into concise, wire-style Markdown briefings, timelines, verification notes, and alerts with fact-analysis separation and confidence labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may auto-apply to broad world-news prompts and impose its own wire-style structure.

Mitigation: Use explicit invocation or ask for a different format when a normal answer is preferred.

Risk: The skill uses an opinionated source hierarchy and confidence-label system for fast-moving news.

Mitigation: Review source choices and confidence labels before relying on outputs for consequential decisions.

Risk: Archival workflows may create or update Markdown files under ./global-wire.

Mitigation: Ask for inline-only output or specify a save path before running archival workflows.

## Reference(s):

- [GlobalWire Skill Page](https://clawhub.ai/yly46967-source/skills/global-wire)
- [Publisher Profile](https://clawhub.ai/user/yly46967-source)
- [Output Modes](references/output-modes.md)
- [Timeline Rules](references/timeline-rules.md)
- [Credibility Rules](references/credibility-rules.md)
- [Source Priority](references/source-priority.md)
- [Formatting Rules](references/formatting-rules.md)
- [File Layout](references/file-layout.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown briefings, timelines, verification notes, and alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Markdown under ./global-wire when requested or when the workflow is archival.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
