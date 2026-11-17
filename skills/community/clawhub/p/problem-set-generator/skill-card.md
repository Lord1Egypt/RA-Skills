## Description:

Generates structured UIBC contest problem drafts for the TH-EVT-002 domain with difficulty options and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Contest organizers and developers use this skill to draft structured UIBC problem sets for committee review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad agent tools despite claiming it needs no network or file access.

Mitigation: Review before installing; remove unused Write and WebFetch access, limit Bash to the local CLI, and clarify activation conditions.

Risk: Template-based problem drafts or claimed contest-rule alignment may be unsuitable for publication without review.

Mitigation: Have the organizing committee verify current rules, refine and deduplicate drafts, and approve each problem before publication.

## Reference(s):

- [Problem Set Generator on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/problem-set-generator)
- [Publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Problem drafts include review status, warnings, and return codes; human review is required before publication.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
