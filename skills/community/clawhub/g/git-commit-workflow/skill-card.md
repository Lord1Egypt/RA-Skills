## Description:

Use when the user wants a single clean commit created from current changes with safe staging, message drafting, and non-interactive git usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they want an agent to inspect current Git changes, stage only relevant files, draft a concise commit message, and create one non-amended commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may stage secrets or unrelated files if the working tree is not reviewed carefully.

Mitigation: Review the current diff and staged files before committing, and stage only files relevant to the requested change.

Risk: A commit workflow can accidentally alter history or bypass expected project checks if broad Git commands are used.

Mitigation: Use non-interactive commands, do not amend or bypass hooks unless explicitly requested, and avoid empty commits.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or plain text with Git command usage and a commit summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a Git commit as a workspace side effect when the agent executes the workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
