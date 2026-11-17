## Description:

Safe code execution in sandboxed environments. Supports Python, JavaScript, Bash, and more with resource limits and timeout controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run code snippets or scripts with stated timeout, memory, network, filesystem, and output constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package describes sandboxed execution, but the reviewed artifact does not include the executor script that would enforce the sandbox and resource limits.

Mitigation: Review package contents before installation and verify a trusted executor implementation before using the skill to run code.

Risk: The documented relative command path could run an unintended local file if a matching path exists in the working directory.

Mitigation: Use explicit trusted paths and inspect the working directory before executing generated commands.

Risk: Running untrusted code can expose systems if sandbox controls are not enforced outside the skill text.

Mitigation: Run code only in an isolated container or virtual machine with network, filesystem, timeout, memory, and output limits enforced by the runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-code-executor)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-shaped execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact describes a 1MB output limit.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
