## Description:

Generates human-readable weekly or monthly reports from an agent's date-named daily memory logs, summarizing activity, project momentum, open threads, and metric changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT

## Use Case:

Agent owners and operators use this skill to review recent work recorded in date-named daily memory logs. It summarizes activity, project momentum, unresolved threads, and metric changes for a selected period; heuristic findings should be checked before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags a broad planning trigger and missing declared tool scope; runtime permission enforcement and scan coverage are uncertain.

Mitigation: Review the trigger scope and confirm the agent's tool permissions before enabling the skill; treat scanner coverage as incomplete.

## Reference(s):

- [Memory Digest on ClawHub](https://clawhub.ai/thomaszhou22/skills/memory-digest)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Markdown report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes a configurable date window; open threads and metrics are heuristic candidates for review.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
