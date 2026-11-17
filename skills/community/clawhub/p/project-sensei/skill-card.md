## Description:

Project Sensei guides agents to teach users how to rebuild software projects from scratch or get existing projects running with beginner-friendly, chapter-style explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinanxrasheed](https://clawhub.ai/user/sinanxrasheed)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, learners, and project maintainers use this skill to have an agent explain a codebase step by step, rebuild it from scratch for teaching, or produce a run diary for local setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect a user-selected project folder.

Mitigation: Use it only on intended project folders and avoid exposing unrelated private files or secrets.

Risk: The skill may suggest setup commands for dependency installation or project execution.

Mitigation: Review commands before running them, especially when the project source is untrusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinanxrasheed/skills/project-sensei)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with chapter-style prose and fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a living journal for rebuilding a project or a chronological run diary for setup.]

## Skill Version(s):

1.0.0 (source: manifest.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
