## Description:

PathwayAtlas helps students, families, and teachers plan China college-admissions choices by gathering an anonymous profile, checking public sources, and comparing schools, majors, and pathway options with evidence-backed next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarry12227](https://clawhub.ai/user/sarry12227)

### License/Terms of Use:

MIT

## Use Case:

Students, families, teachers, and advising agents use this skill to collect the student's planning context, compare China gaokao schools, majors, and alternative admissions pathways, and turn public-source evidence into practical next actions.

### Deployment Geography for Use:

Global, for China higher-education planning contexts

## Known Risks and Mitigations:

Risk: The skill may save an anonymous planning profile, public-source extracts, and generated reports in a private local workspace.

Mitigation: Use it only in a trusted agent environment, avoid entering direct identifiers, and review or delete local workspaces according to the host's data-handling policy.

Risk: Spreadsheet parsing has one hardening gap noted by the security scan.

Mitigation: Avoid untrusted large spreadsheets unless the host provides resource limits and file handling controls; prefer public-source text or smaller verified files.

Risk: The planning output could be mistaken for an admissions guarantee.

Mitigation: Treat recommendations as planning guidance, keep cited source limits visible, and confirm final eligibility and application choices against current official admissions requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarry12227/skills/pathway-atlas)
- [README](README.md)
- [Using PathwayAtlas](docs/using-pathway-atlas.md)
- [Data Sources and Redistribution Policy](DATA_SOURCES.md)
- [Source Policy](references/source-policy.md)
- [Quick Planning Workflow](references/quick-planning.md)
- [Questionnaire](references/questionnaire.md)
- [Education Ministry strong-foundation plan overview](https://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/202001/t20200115_415579.html)
- [Zhejiang three-in-one admissions overview](https://www.zjzs.net/col/col392/index.html)
- [Education Ministry special-admissions topic](https://www.moe.gov.cn/jyb_xwfb/xw_zt/moe_357/2026/2026_zt08/)
- [Public-funded teacher education measures](https://www.moe.gov.cn/jyb_xxgk/moe_1777/moe_1778/202406/t20240614_1135654.html)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Chinese conversational guidance, Markdown reports, structured local evidence and planning files, with optional DOCX export when host capabilities allow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are planning guidance, not admissions guarantees; reports are anonymous and should cite decision-relevant sources.]

## Skill Version(s):

0.2.12 (source: server release; runtime logic version 0.2.9 from pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
