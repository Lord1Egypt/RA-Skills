## Description: <br>
Apply high-fidelity localization to structured artifacts such as web apps, docs, PDFs, slide decks, Office files, subtitles, code repositories, and game assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuki61256-cell](https://clawhub.ai/user/yuki61256-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, localization engineers, and content teams use this skill to localize structured artifacts while preserving layout, placeholders, identifiers, encoding, links, and validation evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The file inventory helper can reveal sensitive filenames if it is pointed at a broad personal or system directory. <br>
Mitigation: Run the probe only on the specific file, project folder, or artifact set intended for localization. <br>
Risk: Structured localization can corrupt placeholders, identifiers, links, layout, or glyph rendering when the source format is not safely round-trippable. <br>
Mitigation: Use the decision thresholds, translation boundaries, format checklist, and quality gates before handoff; stop or narrow scope when safe validation cannot pass. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Decision Thresholds](references/decision-thresholds.md) <br>
- [Artifact Pipelines](references/artifact-pipelines.md) <br>
- [Translation Boundaries](references/translation-boundaries.md) <br>
- [Format Risk Checklists](references/format-risk-checklists.md) <br>
- [Locale-Sensitive Typography](references/locale-sensitive-typography.md) <br>
- [Quality Gates](references/quality-gates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with localized artifacts or repository changes when safe] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a selected pipeline note, protected or skipped items, and a validation summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
