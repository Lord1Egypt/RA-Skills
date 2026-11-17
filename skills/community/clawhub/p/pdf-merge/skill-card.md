## Description:

Merges multiple PDF files locally, with optional compression and metadata editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to merge local PDF files, optionally reduce output size, and set document metadata without uploading files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pdf-lib dependency is not pinned, which can expose users to normal package supply chain drift.

Mitigation: Install dependencies from trusted registries, review resolved package versions, and lock dependency versions for managed deployments.

Risk: Chinese documentation and command output may be harder for non-Chinese readers to review before execution.

Mitigation: Review translated usage instructions and test commands with non-sensitive PDF files before using the skill in a production workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fly3094/skills/pdf-merge)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and local PDF file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local PDF files; requires Node.js and the pdf-lib npm package.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
