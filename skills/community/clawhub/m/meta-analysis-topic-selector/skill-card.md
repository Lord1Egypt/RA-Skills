## Description: <br>
Meta Analysis Topic Finder helps researchers assess, refine, and report candidate systematic review or meta-analysis topics using PICO decomposition, feasibility scoring, deduplication guidance, PRISMA/AMSTAR-2 pre-checks, and structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenhan9739](https://clawhub.ai/user/wenhan9739) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, clinicians, students, and evidence-synthesis teams use this skill to turn a broad research direction into a feasibility-assessed, protocol-ready meta-analysis topic. It supports rapid topic verdicts, full topic reports, deduplication re-audits, and PROSPERO preparation before evidence extraction or synthesis begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated medical-methodology recommendations could be incomplete, outdated, or unsuitable for a specific research protocol. <br>
Mitigation: Have a qualified methodologist or clinical reviewer check topic reports, search plans, PRISMA/AMSTAR-2 judgments, and PROSPERO fields before relying on them. <br>
Risk: The report generator can overwrite the output file path selected by the user. <br>
Mitigation: Choose output paths deliberately, avoid pointing the script at important existing files, and keep a backup or versioned copy of reports. <br>
Risk: Rapid assessments and novelty scores are tentative when deduplication searches have not been completed. <br>
Mitigation: Run the full deduplication workflow across PROSPERO, Cochrane, PubMed, and relevant non-English databases before treating the topic as novel. <br>
Risk: Some evidence sources, especially Cochrane Library results, may require institutional access or manual user searches. <br>
Mitigation: Document which databases were searched, who performed each search, access constraints, search dates, and unresolved gaps in the final topic report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenhan9739/meta-analysis-topic-selector) <br>
- [Topic selection framework](references/topic-selection-framework.md) <br>
- [PICO decomposition guide](references/pico-decomposition-guide.md) <br>
- [Novelty assessment guide](references/novelty-assessment-guide.md) <br>
- [PRISMA 2020 checklist](references/prisma-2020-checklist.md) <br>
- [AMSTAR-2 checklist](references/amstar-2-checklist.md) <br>
- [Topic report template](assets/topic_report_template.md) <br>
- [PROSPERO registration mapping](assets/prospero-registration-mapping.md) <br>
- [PROSPERO](https://www.crd.york.ac.uk/prospero/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or HTML topic reports, rapid verdict cards, score tables, checklists, shell commands, and JSON input configuration for the report generator] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python report generator accepts structured JSON input and writes Markdown or HTML output; missing fields are reported as warnings.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter, evidence.release.version, CHANGELOG dated 2026-06-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
