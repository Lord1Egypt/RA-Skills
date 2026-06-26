## Description: <br>
Collects official Hong Kong master's admissions information, including tuition, deadlines, English requirements, program details, and official links, then formats it as Excel-compatible TSV, Word-compatible HTML, PDF-ready HTML, HTML, or Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, education consultants, and analysts use this prompt-based skill to gather and compare master's admissions information for Hong Kong universities from official university sources. It helps structure admissions data into user-requested report formats for review and planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Admissions data can be outdated, incomplete, or inconsistent with current university pages. <br>
Mitigation: Treat generated admissions reports as drafts and verify every fee, deadline, requirement, program list, and official link directly on the relevant university website. <br>
Risk: The release requests crypto and purchase-related capabilities that are unrelated to an admissions collection workflow. <br>
Mitigation: Do not grant crypto or purchase permissions when using this skill. <br>
Risk: The skill can produce report files in multiple formats, which may overwrite or create local files depending on the host agent. <br>
Mitigation: Require user confirmation before writing or exporting report files. <br>
Risk: The skill claims official and complete coverage, but generated outputs may not prove full coverage. <br>
Mitigation: Audit coverage against the source university list and mark unconfirmed fields clearly before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wscats/hku) <br>
- [README](artifact/README.md) <br>
- [Skill specification](artifact/SKILL-SPEC.md) <br>
- [Data schema](artifact/skill/DATA-SCHEMA.md) <br>
- [Collection prompt](artifact/skill/COLLECTION-PROMPT.md) <br>
- [HKU Graduate School programmes on offer](https://www.gradsch.hku.hk/gradsch/prospective-students/programmes-on-offer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown, HTML, TSV, and structured report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is prompt-only and may produce report files when the user requests export formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
