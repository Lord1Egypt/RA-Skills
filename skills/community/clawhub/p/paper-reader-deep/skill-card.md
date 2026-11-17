## Description:

Paper Reader Deep helps agents extract metadata from PDF papers and generate structured Chinese-language Markdown reading reports with core-understanding, critique, and research-relevance sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jibeilindong](https://clawhub.ai/user/jibeilindong)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and technical readers use this skill to process directories of PDF papers, extract paper metadata and key data, and produce structured Markdown reading reports for later AI-assisted analysis and user research notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads PDFs from a user-supplied directory and writes generated Markdown reports alongside those files.

Mitigation: Run it only on intended directories and review generated report files before sharing or committing them.

Risk: DOI metadata lookup may disclose DOI values to Crossref.

Mitigation: Disable or avoid networked DOI lookup for sensitive unpublished papers, or run the workflow in a controlled offline environment.

Risk: Unpinned Python dependencies can vary across environments.

Mitigation: Install dependencies in a virtual environment and pin versions for stricter or repeatable deployments.

## Reference(s):

- [Paper Reader Deep on ClawHub](https://clawhub.ai/jibeilindong/skills/paper-reader-deep)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one Markdown report per PDF and a summary report in the source PDF directory.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
