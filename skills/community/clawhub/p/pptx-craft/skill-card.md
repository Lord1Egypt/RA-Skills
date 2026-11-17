## Description:

pptx-craft converts structured data, dashboards, reports, and standard HTML into editable PowerPoint decks using text-first layout, template cloning, and QA checks to reduce overlap, clipping, and cramped spacing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanxinluo12345](https://clawhub.ai/user/yuanxinluo12345)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and report authors use this skill to generate editable PPTX decks from structured JSON data, standards-based HTML, or canvas JSON. It is intended for template-aware business reporting workflows that need PowerPoint-native output, preview artifacts, and geometry QA reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release security evidence reports concrete local-file safety concerns around temporary PPT template handling.

Mitigation: Run conversions in an isolated workspace, avoid sensitive templates until temporary-file handling is reviewed, and inspect generated files before sharing them.

Risk: Release security evidence reports a risk of failed-output publication.

Mitigation: Check process exit codes, QA JSON reports, and preview artifacts before trusting or distributing generated PPTX files.

Risk: The skill runs local Python conversion scripts with external dependencies.

Mitigation: Use a pinned dependency set in an isolated environment and process only trusted input files and templates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanxinluo12345/skills/pptx-craft)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with Python scripts that generate editable PPTX files, SVG/PNG previews, QA JSON reports, and input snapshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against user-provided HTML, JSON, and optional PPTX template files; outputs are written to caller-specified local paths.]

## Skill Version(s):

1.2.3 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
