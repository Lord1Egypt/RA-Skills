## Description:

Fetch academic papers from Sci-Hub given a DOI, automatically downloads PDFs, and saves them to research/papers/ with clean filenames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biohackerrrrrr](https://clawhub.ai/user/biohackerrrrrr)

### License/Terms of Use:


## Use Case:

External users, developers, and research automation agents use this skill to retrieve academic-paper PDFs by DOI or PubMed-related requests and save them into a workspace paper library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally contacts Sci-Hub with DOI queries and saves returned PDFs locally.

Mitigation: Install only for workflows where this behavior is intended, and run it in a controlled workspace.

Risk: The skill saves unvalidated remote PDF files and has under-scoped file-writing behavior.

Mitigation: Set the output directory explicitly, avoid shared or privileged directories, and treat downloaded PDFs as untrusted files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biohackerrrrrr/skills/paper-fetcher)
- [Sci-Hub domain configured by skill](https://www.sci-hub.su)
- [DOI resolver](https://doi.org/)

## Skill Output:

**Output Type(s):** [text, files, shell commands]

**Output Format:** [PDF files saved locally with brief text confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are named paper_[DOI with slashes replaced].pdf; downloaded PDFs should be treated as untrusted files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
