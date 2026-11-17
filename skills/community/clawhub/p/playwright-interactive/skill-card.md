## Description:

Persistent browser and Electron interaction through js_repl for fast iterative UI debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tridefender](https://clawhub.ai/user/tridefender)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep Playwright browser or Electron sessions alive while debugging local user interfaces, running functional checks, and capturing visual QA evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to disable sandbox protection for Playwright and js_repl use.

Mitigation: Use the skill only in trusted local workspaces and prefer an isolated VM or container when testing unfamiliar code.

Risk: The workflow installs runtime dependencies and may launch local web or Electron applications.

Mitigation: Avoid unknown repositories, pull requests, downloaded Electron apps, and environments containing sensitive credentials.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill and its dependencies before deployment, and use pinned dependencies where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tridefender/skills/playwright-interactive)
- [ClawHub publisher profile](https://clawhub.ai/user/tridefender)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with JavaScript, shell, and TOML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for persistent Playwright and Electron QA sessions; it does not produce standalone application artifacts.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
