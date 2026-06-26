## Description: <br>
Math Guide Solver helps agents extract math from images or text, normalize formulas to LaTeX, render formulas as PNGs, and provide Socratic, detailed, or quick solution guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yshajoy](https://clawhub.ai/user/yshajoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, teachers, tutors, and agent developers use this skill to turn math problem images, markdown, or text into extracted formulas, rendered mathematical notation, and solution guidance across common math domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included GitHub update script can alter and publish a repository using local credentials if run. <br>
Mitigation: Review the script and run it only in an intended repository with appropriate credentials and branch protections. <br>
Risk: Math images or notes may contain homework, student records, or personal information that could be processed by OCR or model integrations. <br>
Mitigation: Avoid submitting sensitive educational or personal data unless the deployment's data-handling terms and retention controls are acceptable. <br>
Risk: OCR and LaTeX conversion can misread formulas, especially for poor handwriting, complex diagrams, or incomplete problems. <br>
Mitigation: Ask users to verify extracted formulas and rerun with clearer images or manual LaTeX input when confidence is low. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yshajoy/math-guide-solver) <br>
- [SKILL.md](SKILL.md) <br>
- [Math Solver Installation & Quick Start](references/QUICKSTART.md) <br>
- [EXAMPLES.md](references/EXAMPLES.md) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, PNG images, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON guidance with optional PNG formula renderings and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Socratic, detailed, and quick modes; configurable themes, formula size, DPI, language, and batch processing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and changelog, released 2026-03-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
