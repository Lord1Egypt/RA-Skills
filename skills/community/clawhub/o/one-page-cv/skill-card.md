## Description: <br>
Generate professionally tailored, one-page LaTeX/PDF resumes customized for specific job applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy8647](https://clawhub.ai/user/andy8647) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers and career-support agents use this skill to tailor an existing resume or supplied background to a target job description, then produce a single-page ATS-friendly LaTeX/PDF resume. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated resume claims, metrics, names, or language choices may be unsupported or inaccurate. <br>
Mitigation: Review every claim and metric before using the resume, and replace unsupported estimates with verified facts. <br>
Risk: The skill can inspect resume files from the working directory on broad career-related triggers. <br>
Mitigation: Confirm which resume or background files should be used and keep unrelated sensitive documents out of the working directory. <br>
Risk: Environment setup may propose package installs, font downloads, or file moves. <br>
Mitigation: Approve only the exact commands and file operations needed for the task after checking their targets. <br>
Risk: Generated PDFs and LaTeX files may contain personal contact, education, and employment information. <br>
Mitigation: Store outputs in controlled locations and review the generated PDF before sharing it with employers or third parties. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/andy8647/one-page-cv) <br>
- [Publisher profile](https://clawhub.ai/user/andy8647) <br>
- [LaTeX Resume Template Reference](references/latex-template.md) <br>
- [Maple Font](https://github.com/subframe7536/maple-font) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, LaTeX source, shell commands, and generated PDF resume files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a .tex/ working folder, compile with XeLaTeX, move a generated PDF to the working directory, and clean LaTeX intermediate files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
