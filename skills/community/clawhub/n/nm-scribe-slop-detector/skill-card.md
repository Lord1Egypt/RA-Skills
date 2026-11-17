## Description:

Detects AI-generated writing patterns in prose

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and documentation maintainers use the skill to review prose for concentrated AI-writing patterns, identity leaks, unsupported claims, and structural issues. It produces findings and suggested edits for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports cleanup and network-check behavior beyond the skill's stated prose-detection purpose.

Mitigation: Review the complete behavior and use the skill only when that broader scope is needed.

Risk: The security review reports incomplete inspection: 18 of 21 components were fully inspected, with parser or output limits and missing referenced paths.

Mitigation: Review the uninspected components and unavailable referenced material before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-slop-detector)
- [Scribe plugin homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown audit reports or structured JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings can include file and line locations, category, severity, confidence, rationale, and proposed fixes; low-confidence findings are surfaced for human review.]

## Skill Version(s):

1.10.3 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
