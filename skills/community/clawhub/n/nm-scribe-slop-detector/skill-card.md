## Description:

Detects AI-generated writing patterns in prose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use this skill to review prose and code comments for AI-style wording and structural patterns. It reports located findings and suggests fixes for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with high confidence and reports broad project changes that may not match the prose-analysis purpose.

Mitigation: Review the skill's scope and requested permissions before installation or execution; the security guidance advises avoiding installation until reviewed.

Risk: The security evidence reports persistent configuration edits, remote pushes, and document-triggered network checks; scanner coverage is partial.

Mitigation: Inspect these actions and network checks, and account for the stated coverage gaps before using the skill.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-scribe-slop-detector)
- [Project homepage (metadata.clawdis)](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)
- [Publisher profile (athola)](https://clawhub.ai/user/athola)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown report or JSON in CI mode, with file and line references, findings, severity, confidence, evidence, and suggested fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are surfaced for human review; low-confidence findings should not be applied automatically.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
