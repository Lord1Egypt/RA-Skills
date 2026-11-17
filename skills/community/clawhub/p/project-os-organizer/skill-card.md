## Description:

Privacy-first, chat-first project manager for vibe coders. Track projects, capture updates, and resume work across local folders, Claude/Codex, and GitHub with explicit opt-in controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldodee](https://clawhub.ai/user/ldodee)

### License/Terms of Use:


## Use Case:

Developers and AI-assisted builders use this skill to maintain a local-first inventory of active projects, capture progress and next steps, review recent activity, and resume work from local folders, chat sessions, and optional GitHub signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project discovery can scan broad local folders and, when explicitly enabled, chat transcript roots.

Mitigation: Set PROJECT_OS_ROOT to a reviewed local checkout and keep chat indexing and home discovery disabled unless they are needed.

Risk: The skill keeps persistent organizer state and generated memory files under ~/.project_os.

Mitigation: Review the configured database, config, logs, and memory paths before using the skill on sensitive projects.

Risk: Dashboard workflows can start, restart, or stop a localhost service on the configured port.

Mitigation: Use a reviewed PROJECT_OS_PORT and avoid dashboard restart or stop actions on ports used by other local services.

Risk: Optional remote install and GitHub sync expand execution and data-access scope.

Mitigation: Keep remote install and GitHub sync disabled unless explicitly required, and review the target checkout and token environment before enabling them.

## Reference(s):

- [Project Definition](references/project-definition.md)
- [Workflow](references/workflow.md)
- [Project OS Organizer on ClawHub](https://clawhub.ai/ldodee/skills/project-os-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with optional shell command snippets, dashboard URLs, and machine-readable smoke-result lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local organizer state, configuration, logs, and memory snapshots under ~/.project_os when the user runs the skill workflows.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
