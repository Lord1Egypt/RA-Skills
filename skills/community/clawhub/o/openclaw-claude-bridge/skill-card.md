## Description:

Bridges OpenClaw to a locally installed Claude Code CLI for code generation, code review, and data analysis without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cry779](https://clawhub.ai/user/cry779)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and execute local Claude Code tasks for code generation, code review, and data analysis from OpenClaw workflows. It supports both manual shell-script execution and automated Python execution when Claude Code is installed, logged in, and backed by a valid subscription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant broad local read, edit, and shell execution power through Claude Code.

Mitigation: Install only in a trusted, sandboxed environment and restrict Claude tools and working directories before use.

Risk: The skill builds executable shell scripts from prompts, which can make untrusted prompt content unsafe.

Mitigation: Review generated or packaged task scripts before execution and avoid running tasks created from untrusted prompts.

Risk: Code or prompts may be sent through the configured Claude provider or proxy during execution.

Mitigation: Review data sensitivity before use and remove secrets or private source content that should not leave the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cry779/skills/openclaw-claude-bridge)
- [Publisher profile](https://clawhub.ai/user/cry779)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON task metadata, generated shell scripts, and captured text or Markdown command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a locally installed and logged-in Claude Code CLI; default local execution timeout is 300 seconds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
