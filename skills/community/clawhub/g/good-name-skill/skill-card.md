## Description:

A naming assistant for Chinese personal names, English personal names, company or brand names, and iterative renaming under new constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenyangze](https://clawhub.ai/user/zhenyangze)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate candidate names for people, English identities, companies, brands, or product lines after collecting key constraints. It produces concise naming options with meanings, fit rationale, risk notes, and recommendation levels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced naming rule documents are absent from the packaged artifact, which can weaken trademark, legal, cultural, or naming-risk guidance.

Mitigation: Treat risk comments as heuristic guidance only, ask for missing context when needed, and require formal legal, trademark, cultural, or naming review before relying on outputs for high-stakes use.

Risk: Generated names may include misleading implications, cultural ambiguity, high similarity, or unresolved regional concerns.

Mitigation: Keep uncertainty visible in the output, avoid claiming official clearance, and validate candidate names against the intended region, language, market, and use case.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/zhenyangze/good-name-skill/tree/main/good-name-skill)
- [ClawHub skill page](https://clawhub.ai/zhenyangze/skills/good-name-skill)
- [Publisher profile](https://clawhub.ai/user/zhenyangze)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with structured candidate lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each candidate includes a name, brief meaning, fit rationale, risk note, and recommendation level.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
