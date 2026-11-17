## Description:

Adds "Made In China" text to Amazon FBA product label PDFs in batch, with placement guidance for single-label and mixed-label PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hipeterjiang](https://clawhub.ai/user/hipeterjiang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operations teams use this skill to prepare Amazon FBA label PDFs by adding country-of-origin text beneath product or barcode-related label content. The workflow supports preview generation, y-position adjustment, and full PDF processing after placement review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow instructs agents to install an unpinned PyPDF2 package with sudo, which grants more system authority than the task requires.

Mitigation: Review before installation, use an isolated environment with a pinned dependency, and avoid passwordless sudo unless the dependency path has been controlled and reviewed.

Risk: The artifact references a PDF processing script path, while the provided release evidence contains only the skill instructions.

Mitigation: Confirm the referenced processing script is present, reviewed, and scoped to the expected PDF-labeling behavior before relying on the workflow.

## Reference(s):

- [Server-resolved source repository](https://github.com/hipeterjiang/pdf-label-made-in-china)
- [ClawHub skill page](https://clawhub.ai/hipeterjiang/skills/pdf-label-made-in-china)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated PDF file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include preview-page generation before full PDF processing.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
