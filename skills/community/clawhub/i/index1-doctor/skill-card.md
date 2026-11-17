## Description:

Diagnoses an index1 environment by checking Python, Ollama, model availability, and index health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gladego](https://clawhub.ai/user/gladego)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to verify an index1 setup, inspect index status, check local embedding model availability, and get fix recommendations when search or vector indexing behaves unexpectedly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested installation commands can download scripts or install packages on the user's machine.

Mitigation: Review official installation documentation, inspect downloaded scripts before execution, and approve package installation only when it matches the intended environment.

Risk: Suggested indexing commands can process local project files.

Mitigation: Run indexing commands only against projects and directories the user intends to index.

## Reference(s):

- [index1 Doctor ClawHub skill page](https://clawhub.ai/gladego/skills/index1-doctor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
