## Description:

Supports writing and revising Chinese-language job descriptions that are candidate-facing, searchable, and aligned with screening and interview criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soulzhong](https://clawhub.ai/user/soulzhong)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, and recruiting operations teams use this skill to draft or improve Chinese job descriptions for different companies, products, industries, seniority levels, and role types. It helps convert internal role language into candidate-facing titles, responsibilities, requirements, bonus qualifications, and optional interview focus notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask an agent to persistently update skill files after reusable user feedback, which may change future behavior beyond the current JD task.

Mitigation: Run installed skills read-only by default, and require an explicit diff plus maintainer approval before allowing updates to SKILL.md, EVOLUTION.md, or related skill guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soulzhong/skills/jd-writing)
- [Title conversion guidance](artifact/title-conversion.md)
- [Verifiable requirements guidance](artifact/verifiable-requirements.md)
- [Role type playbooks](artifact/role-type-playbooks.md)
- [Positioning templates](artifact/positioning-templates.md)
- [Evolution log](artifact/EVOLUTION.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown job descriptions and concise review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional reverse-screening language and internal interview focus notes when appropriate.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
