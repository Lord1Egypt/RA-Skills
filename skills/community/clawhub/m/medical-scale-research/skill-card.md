## Description:

Retrieves medical scale information and generates standardized reports covering background, copyright, CDISC mapping, statistical methods, Feishu document creation, and knowledge-base archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinget-svg](https://clawhub.ai/user/kevinget-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical researchers, biostatisticians, medical research teams, and pharmaceutical developers use this skill to retrieve public medical-scale information, organize evidence, recommend CDISC SDTM/ADaM mappings, and produce standardized research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download or upload full medical scale materials, which may be copyrighted or access-restricted.

Mitigation: Use only materials the user is authorized to download or upload, confirm copyright and licensing terms, and restrict Feishu permissions and knowledge-base destinations.

Risk: The skill describes unsafe shell downloading with curl and a hard-coded local save path.

Mitigation: Replace ad hoc shell downloads with a safer download method and change the save path to a user-approved workspace location before use.

Risk: Generated CDISC mappings, statistical methods, and medical-scale summaries may be incomplete or inaccurate.

Mitigation: Require qualified clinical, statistical, and data-standards review before using outputs in regulated research or submissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kevinget-svg/skills/medical-scale-research)
- [Scale Report Template](artifact/templates/scale-report.md)
- [CDISC Mapping Rules](artifact/rules/cdisc-mapping.json)
- [SGRQ Example Report](artifact/examples/SGRQ-example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report text with Feishu document links and inline SAS/R or shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download official scale PDFs or capture screenshots and publish report content to Feishu and a knowledge base when the user has authorization.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
