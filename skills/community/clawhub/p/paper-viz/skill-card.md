## Description:

Paper Viz extracts experimental results from research PDFs, screenshots, and table images, selects suitable chart types, generates deterministic Python figures, and exports PNG, PDF, and LaTeX outputs into a paper-named folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghxianzhi](https://clawhub.ai/user/ghxianzhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to turn paper result tables, screenshots, and PDFs into reproducible chart assets with extracted data, publication-style figures, and LaTeX snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted values from papers, screenshots, or tables may be uncertain or unreadable.

Mitigation: Review experimental_data.json, especially entries marked validation_needed, before relying on generated figures.

Risk: The workflow creates folders and writes generated chart files locally.

Mitigation: Provide a clear input file and output root directory, then review the final saved folder path and generated files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [JSON data, PNG/PDF figure files, LaTeX snippets, Python plotting code, and a concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes outputs to a local paper-named folder when possible and marks extracted data with validation_needed when confidence is low.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
