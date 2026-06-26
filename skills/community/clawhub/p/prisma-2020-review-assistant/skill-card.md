## Description: <br>
Review, audit, coach, and extract PRISMA 2020 reporting compliance for systematic reviews, meta-analyses, protocols, reviewer comments, and draft manuscript sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors, reviewers, and research teams use this skill to assess draft systematic reviews or protocols against PRISMA 2020, produce checklist audit tables, locate manuscript evidence, and draft fixes for reporting gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PRISMA assessments may be incomplete or misleading when the user provides only excerpts, an abstract, or ambiguous manuscript text. <br>
Mitigation: Treat assessments as provisional for partial inputs and require visible manuscript evidence for each checklist judgment. <br>
Risk: Checklist guidance may affect scholarly reporting or submission decisions. <br>
Mitigation: Have a human author or reviewer confirm PRISMA interpretations, manuscript evidence, and journal-specific requirements before submission. <br>
Risk: Agent-proposed actions could be inappropriate if accepted without review in sensitive repositories or documents. <br>
Mitigation: Review suggested changes and any command execution before approval, especially around secrets, production configuration, or publication-critical text. <br>


## Reference(s): <br>
- [PRISMA 2020 map for manuscript review](references/prisma-2020-map.md) <br>
- [PRISMA 2020 checklist source extraction](references/prisma-2020-checklist-source.md) <br>
- [PRISMA 2020 expanded checklist source extraction](references/prisma-2020-expanded-checklist-source.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prioritized findings, section-by-section PRISMA assessments, checklist tables, evidence maps, and revision guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
