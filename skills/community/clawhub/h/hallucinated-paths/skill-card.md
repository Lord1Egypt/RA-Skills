## Description:

Reply cites file paths, directories, or module locations that do not exist in the current project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to avoid citing or editing non-existent files, directories, or module paths. It guides the agent to verify paths with local file checks and to state clearly when a required path cannot be found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may still mention a plausible but non-existent path if it skips verification.

Mitigation: Verify paths with local file checks or repository search before citing or editing them, and state when a path cannot be found.

Risk: Additional local file searches may inspect more project files than needed.

Mitigation: Keep searches scoped to the current project and the specific symbol, filename, or directory being discussed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scoped file-existence checks and explicit not-found statements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
