## Description: <br>
Writes and polishes English graduate admissions CVs and resumes from education, research, internship, project, awards, and skills information, with optional PDF export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[offerclaw](https://clawhub.ai/user/offerclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Applicants and advisors use this skill to collect admissions CV material, draft or polish an English graduate-school CV, check quality, and optionally export a PDF after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles personal CV details such as contact, education, and experience history. <br>
Mitigation: Keep processing local where possible, include only necessary personal details, and review the final CV before sharing it. <br>
Risk: PDF export installs third-party Python packages on first use. <br>
Mitigation: Run export only in an environment where installing the documented Python dependencies is acceptable. <br>
Risk: PDF export can add an OfferClaw footer watermark by default. <br>
Mitigation: Check exported PDFs before submission and use the documented watermark-off option when branding is not wanted. <br>


## Reference(s): <br>
- [CV Information Requirements](references/info-requirements.md) <br>
- [CV Writing Instructions](references/writing-instructions.md) <br>
- [CV Format Example](references/cv-format-example.md) <br>
- [CV Quality Checklist](references/quality-checklist.md) <br>
- [Bullet Expansion Guide](references/bullet-expansion-guide.md) <br>
- [PDF Export Scripts](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Conversational guidance, plain-text CV drafts, tagged Markdown, and optional PDF export commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a tagged Markdown CV file and export a PDF locally after the user confirms the final content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
