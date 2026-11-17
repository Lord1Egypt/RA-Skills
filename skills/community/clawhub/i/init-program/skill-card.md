## Description:

Create or update the correct agent instruction file for the active coding assistant, then initialize a software project according to that file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dreamingphper](https://clawhub.ai/user/dreamingphper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to create or update repository agent instructions, then bootstrap a project according to the selected instruction file and verified workspace evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent instruction files can influence future assistant behavior in the repository.

Mitigation: Review any generated AGENTS.md or CLAUDE.md before relying on it for future project work.

Risk: Project initialization can create or update local repository files.

Mitigation: Inspect proposed changes and confirm ambiguous requirements before running mutating commands or accepting generated project structure.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated or updated repository files and shell commands when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update agent instruction files such as AGENTS.md or CLAUDE.md, then initialize project files according to confirmed requirements.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
