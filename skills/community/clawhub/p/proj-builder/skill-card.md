## Description:

Generates structured project scaffolds and template files for Node.js, Python, and Go through bash commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create starter project structures for Node.js, Python, and Go applications, or to inspect representative template files before scaffolding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The init command can overwrite template files in any writable path supplied by the user or agent.

Mitigation: Review the destination before running init, use a fresh project directory, and avoid absolute or parent-directory paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/proj-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with shell commands and generated source or configuration file contents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The init command can create or replace files in the project directory supplied by the user or agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
