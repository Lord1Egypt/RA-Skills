## Description: <br>
MinerU Fast Extract converts PDFs, images, Word documents, and PowerPoint presentations into Markdown using the mineru-open-api CLI, with OCR, table recognition, and formula extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mineru-extract](https://clawhub.ai/user/mineru-extract) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, students, and document-heavy teams use this skill to extract Markdown from local documents or remote document URLs without configuring API keys or accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local documents or remote document URLs to an external MinerU API for processing. <br>
Mitigation: Use it only with documents and URLs approved for external processing, avoid confidential files or token-bearing URLs, and clean up generated output directories when the extracted content should not persist. <br>


## Reference(s): <br>
- [MinerU Fast Extract on ClawHub](https://clawhub.ai/mineru-extract/mineru-fast-extract) <br>
- [MinerU homepage](https://mineru.net) <br>
- [Source link from skill metadata](https://github.com/MinerU-Extract/mineru-fast-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown output to stdout or saved files, with extracted images saved alongside Markdown when an output path is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tables are rendered as Markdown tables, formulas as LaTeX, and progress or status messages are sent to stderr.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
