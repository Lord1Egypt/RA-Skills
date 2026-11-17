## Description:

KiloCode is an AI coding agent CLI skill for generating code from natural language, refactoring and debugging projects, automating development workflows, and running terminal commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weinguyen1224-glitch](https://clawhub.ai/user/weinguyen1224-glitch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate coding tasks to the KiloCode CLI, including code generation, refactoring, debugging, test execution, and CI/CD automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous mode can run commands and change files without interactive permission prompts.

Mitigation: Use autonomous mode only in trusted, backed-up, least-privilege environments.

Risk: Delegated coding work can introduce incorrect code, unsafe commands, or unwanted file changes.

Mitigation: Review proposed changes, commands, and scan results before deploying outputs.

## Reference(s):

- [Kilo documentation](https://kilo.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file edits and terminal automation when the KiloCode CLI is invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
