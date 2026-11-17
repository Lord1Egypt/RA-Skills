## Description:

Complete mathematical problem solving workflow with OCR, LaTeX formula extraction, PNG rendering, and guided solutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yshajoy](https://clawhub.ai/user/yshajoy)

### License/Terms of Use:

MIT-0

## Use Case:

Students, teachers, tutors, and developers use this skill to extract math from images or text, render LaTeX formulas, and produce Socratic hints, detailed explanations, or quick answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes release automation that can modify files, create tags, and push to GitHub, which is outside ordinary math-solving behavior.

Mitigation: Do not run GITHUB_UPDATE_SCRIPT.sh unless you are the maintainer and have verified the repository, source files, staged diff, and tag policy.

Risk: Uploaded images or documents may contain sensitive content and can be processed by OCR, LLM, or optional API services.

Mitigation: Avoid uploading sensitive images or documents unless that processing path is acceptable for the data.

Risk: OCR, LaTeX extraction, and generated solution guidance can misread handwriting or formulas and produce incorrect math.

Mitigation: Review extracted formulas, validate final answers, and request clearer input or manual LaTeX when confidence is low.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yshajoy/skills/math-guide-solver)
- [Quick Start Guide](references/QUICKSTART.md)
- [Usage Examples](references/EXAMPLES.md)
- [Changelog](CHANGELOG.md)
- [README v1.1.0](README_v1.1.0.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown, JSON, HTML, PNG file references, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process uploaded images or documents through OCR and optional APIs; formula images may be embedded as base64 in HTML or JSON outputs.]

## Skill Version(s):

1.1.0 (source: server release metadata, target metadata, changelog released 2026-03-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
