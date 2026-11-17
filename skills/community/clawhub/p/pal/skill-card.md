## Description:

Analyze any project directory and produce a detailed report covering what the project does, its tech stack, folder structure, entry points, how to run it, and where to start reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g30tr1x](https://clawhub.ai/user/g30tr1x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get oriented in unfamiliar project directories by scanning local files and summarizing the project purpose, technology stack, structure, entry points, and run commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads project files from the directory the user selects, which can expose private or sensitive content to the agent session.

Mitigation: Run it only on intended project directories and avoid broad home, company, or secrets-heavy paths.

Risk: Scanned project files may contain untrusted instructions or prompt-injection content.

Mitigation: Treat file contents as project evidence only and review generated commands or guidance before acting on them.

## Reference(s):

- [Project Analyzer on ClawHub](https://clawhub.ai/g30tr1x/skills/pal)
- [Project Analyzer README](artifact/README.md)
- [Project Analyzer Skill Definition](artifact/SKILL.md)
- [Python 3 Downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with concise sections and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local Python scanner over the requested project directory and returns a human-readable orientation report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
