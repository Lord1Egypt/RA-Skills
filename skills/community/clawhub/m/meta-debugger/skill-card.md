## Description:

AI-powered self-debugging system that identifies, analyzes, and fixes errors automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add local Python error handling, root cause analysis, fix suggestions, and error-pattern tracking to agent or application workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags the published install command as an avoidable package-installation risk.

Mitigation: Review installation steps before use; remove the unnecessary pip install step for standard-library modules or install only in an isolated environment.

Risk: The skill can be configured with automatic fixing behavior, which may produce incorrect or unsuitable remediation choices.

Mitigation: Keep safe mode enabled by default, review suggested fixes manually, and validate changes with tests before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/skills/meta-debugger)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Python helper returns dictionaries containing error analysis, fix candidates, handling results, metrics, and prevention suggestions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
