## Description:

Audit and repair an AI agent's memory corpus for consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT

## Use Case:

Agent developers and operators use this skill to audit Markdown memory files for stale or conflicting facts, missing file references, gaps in dated entries, and unreferenced files. It reports findings for review; edits require confirmation and are made separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unclear activation and file-reading boundaries.

Mitigation: Review when the skill activates and confirm the selected memory workspace before running it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thomaszhou22/skills/memory-checkup)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Plain-text report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit findings; proposed fixes are reviewed and applied separately.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
