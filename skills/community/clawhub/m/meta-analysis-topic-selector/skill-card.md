## Description:

Helps researchers assess meta-analysis topic feasibility and generate structured topic reports with PICO/PECO decomposition, deduplication checks, and PRISMA 2020/AMSTAR-2 previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenhan9739](https://clawhub.ai/user/wenhan9739)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, and evidence-synthesis teams use this skill to turn a vague review idea or candidate PICO into a rapid verdict, deduplication audit, or PROSPERO-ready topic report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rapid assessments can produce tentative feasibility or novelty conclusions before deduplication searches are complete.

Mitigation: Treat rapid verdicts as provisional and complete the full deduplication workflow before relying on the topic decision.

Risk: Generated methodology recommendations or report sections could be incorrect or misleading for a specific research question.

Mitigation: Have domain and evidence-synthesis reviewers check the PICO, scoring rationale, deduplication judgment, and PRISMA/AMSTAR-2 preview before use.

Risk: The skill can create local report files from research inputs.

Mitigation: Use project-specific output paths and review generated files before sharing or submitting them.

## Reference(s):

- [Meta-analysis Topic Selection Methodology Framework](artifact/references/topic-selection-framework.md)
- [PICO/PECO Element Decomposition Guide](artifact/references/pico-decomposition-guide.md)
- [Innovation and Deduplication Assessment Guide](artifact/references/novelty-assessment-guide.md)
- [PRISMA 2020 Checklist](artifact/references/prisma-2020-checklist.md)
- [AMSTAR-2 Assessment Checklist](artifact/references/amstar-2-checklist.md)
- [PROSPERO Registration Form Field Mapping](artifact/assets/prospero-registration-mapping.md)
- [Topic Report Generator Input Example](artifact/scripts/generate_topic_report.example.json)
- [ClawHub Skill Page](https://clawhub.ai/wenhan9739/skills/meta-analysis-topic-selector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text guidance, Markdown or HTML topic reports, and JSON-backed report generation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report generation uses local input and output files; rapid assessments are tentative until deduplication searches are completed.]

## Skill Version(s):

1.0.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
