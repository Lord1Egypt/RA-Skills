## Description:

Searches local iFA Evolution help documentation to locate topics, choose the best matching HTML page, and summarize functions, parameters, usage, returns, and notes in Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers who use iFA Evolution local help files can use this skill to answer targeted documentation questions, locate the relevant HTML topics, and compare similar commands or function blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on hardcoded local Windows paths and reference files that may not exist in every installation.

Mitigation: Confirm the iFA Evolution help directory and topic index path before use, and update paths or regenerate the index for the installed version.

Risk: The reviewed artifact contains encoding damage that may obscure parts of the workflow text.

Mitigation: Normalize the skill text and verify referenced helper files before relying on it for production documentation lookup.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with PowerShell command examples and structured Chinese summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local iFA Evolution help files and a topic index on matching Windows paths.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
