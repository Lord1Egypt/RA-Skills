## Description:

Helps agents generate, repair, and export Microsoft PowerPoint PPTX decks while preserving slide layouts, placeholders, charts, images, speaker notes, and template fidelity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Presentation designers, consultants, educators, analysts, and developers use this skill to diagnose, generate, repair, and validate PPTX decks. It is intended for work that needs reliable slide masters, placeholders, charts, images, speaker notes, branded templates, and presentation-safe rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated code or edited PPTX files may unintentionally alter important presentations, layouts, media, charts, or speaker notes.

Mitigation: Review generated code and edited decks before use, keep the original deck, and perform visual validation in PowerPoint or an equivalent renderer.

Risk: Direct OOXML changes can break relationships between slide parts, layouts, notes, charts, embedded workbooks, or media.

Mitigation: Inspect the relevant PPTX parts and relationships before editing, prefer supported python-pptx operations when available, and validate slide count, placeholders, chart data, notes, and embedded assets afterward.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/powerpoint-pptx-layout-export-helper)
- [PowerPoint automation with Python](https://segmentfault.com/a/1190000047186829)
- [AI office automation for PowerPoint](https://segmentfault.com/a/1190000047541288)
- [python-pptx slide copying discussion](https://segmentfault.com/q/1010000021456549/a-1020000021466136)
- [PowerPoint file automation article](https://segmentfault.com/a/1190000044782876)
- [PowerPoint thumbnail automation discussion](https://segmentfault.com/q/1010000018112239/a-1020000018116097)
- [PPTX speaker notes XML mapping article](https://segmentfault.com/a/1190000047686362)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with optional code snippets, shell commands, configuration notes, and PPTX file artifacts when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a deck diagnosis, repair plan, validation notes, or edited PPTX artifacts; original decks should be retained for review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
