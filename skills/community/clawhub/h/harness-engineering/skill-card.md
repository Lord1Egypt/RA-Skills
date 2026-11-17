## Description:

Evolve existing repositories toward Harness Engineering by making them more legible to agents, moving critical knowledge into repo-local artifacts, adding predictable structure, and replacing policy-only documentation with executable checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doanbactam](https://clawhub.ai/user/doanbactam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to audit and improve existing repositories for agent legibility, repo-local source-of-truth documentation, executable governance checks, and CI enforcement without forcing broad rewrites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation may apply the skill when repository documentation or governance work overlaps with its trigger behavior.

Mitigation: Review proposed changes carefully and disable implicit invocation if the skill should only run when explicitly named.

Risk: The skill may edit AGENTS.md, docs, package scripts, or CI workflows, which can affect contributor workflows.

Mitigation: Review those files before merge and run the repository's local validation and CI checks after changes.

## Reference(s):

- [Harness Template Checklist](references/checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with code, configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or make repository documentation, validation script, package script, and CI workflow changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
