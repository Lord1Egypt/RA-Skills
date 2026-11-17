## Description:

Clone and analyze GitHub project code quality using DeepSeek AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woaim65](https://clawhub.ai/user/woaim65)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze public GitHub repositories for project structure, code quality, potential bugs, security issues, and improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unsafe shell clone command on a repository URL.

Mitigation: Use only public, non-sensitive repositories in a sandbox with no valuable local files or credentials; fix the implementation to use spawn or execFile with strict GitHub URL validation.

Risk: Sampled repository code is sent to an external API without precise disclosure or consent.

Mitigation: Disclose the external API recipient and transmitted data, and require user consent before sending code to any third party.

Risk: A credential-like value is embedded in the artifact.

Mitigation: Remove the embedded value and use managed secrets or user-provided credentials instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/woaim65/skills/github-code-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns repository structure, code quality observations, bug and security issue identification, and improvement suggestions; may fall back to structure-only analysis if the external analysis API fails.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
