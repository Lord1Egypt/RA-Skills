## Description:

Generates tailored, ATS-friendly one-page LaTeX/PDF resumes for specific job applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy8647](https://clawhub.ai/user/andy8647)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to tailor resume content to a target job description and produce a polished one-page PDF. It is designed for role-specific resume generation in English or Chinese using LaTeX and XeLaTeX.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local resume-like files while looking for source material.

Mitigation: Provide the exact resume file and job description to use, and review any discovered files before allowing the agent to read them.

Risk: The skill may propose TeX or font installation steps that change the local system environment.

Mitigation: Review and approve installation commands explicitly, and decline automatic dependency or font installation when not needed.

Risk: The skill may estimate or generate quantified resume metrics when exact numbers are missing.

Mitigation: Verify all generated metrics and claims against the user's real experience before using the resume.

## Reference(s):

- [LaTeX Resume Template Reference](references/latex-template.md)
- [Maple Font](https://github.com/subframe7536/maple-font)
- [One Page CV on ClawHub](https://clawhub.ai/andy8647/skills/one-page-cv)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with LaTeX source, shell commands, and generated PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a .tex working folder, compile with XeLaTeX, move the final PDF to the workspace root, and remove intermediate LaTeX build files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
