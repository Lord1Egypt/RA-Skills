## Description:

Ppt Agent helps users turn a presentation topic into an outline, planning draft, and editable Bento Grid SVG slides that can be imported into PowerPoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianchangnorth](https://clawhub.ai/user/tianchangnorth)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to draft Chinese-focused presentations from a topic through a guided workflow: confirm style, generate an outline, prepare a page plan, and produce editable SVG slide pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional JSON-to-SVG script can turn untrusted JSON into active SVG files without sanitizing content.

Mitigation: Use only trusted input JSON with the optional generator, review generated SVG before opening it in active viewers, and avoid SVG content from unknown sources.

## Reference(s):

- [Ppt Agent on ClawHub](https://clawhub.ai/tianchangnorth/skills/ppt-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON outline blocks, planning text, and SVG code output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final SVG pages target a 1280 by 720 viewBox and PowerPoint-importable vector output.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
