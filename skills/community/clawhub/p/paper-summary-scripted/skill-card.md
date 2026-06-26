## Description: <br>
Downloads arXiv PDFs or reads local paper files, extracts and cleans paper text with a bundled preprocessing script, then generates summary, detailed, contribution, and consistency-check sections in the requested language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crw0149](https://clawhub.ai/user/crw0149) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to run a repeatable paper summarization workflow for arXiv PDFs or local paper files. It is intended for manifest-aware summarization where source extraction status and missing evidence are surfaced before the final answer is trusted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python preprocessing script downloads arXiv PDFs or reads selected local files and writes downloaded PDFs, extracted text, and combined text under the chosen output directory. <br>
Mitigation: Run it only on papers you intend to process, avoid private or unrelated local files, and review the generated manifest and output directory before sharing results. <br>
Risk: PDF, DOCX, or text extraction can fail or be partial, which can make generated summaries incomplete or less reliable. <br>
Mitigation: Use the manifest status, notes, and missing-or-uncertain section to lower confidence or stop generation when extraction is incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crw0149/paper-summary-scripted) <br>
- [Script usage](references/script-usage.md) <br>
- [Prompt mapping](references/prompts.md) <br>
- [Output template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with per-paper sections and preprocessing status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps papers separate unless comparison is requested and includes consistency scores plus error lists for generated sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
