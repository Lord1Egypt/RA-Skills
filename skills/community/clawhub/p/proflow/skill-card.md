## Description:

Proflow standardizes project delivery by guiding agents through requirement brainstorming, execution planning, implementation, specification writing, requirement ID management, document naming, and stage tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1232023](https://clawhub.ai/user/luis1232023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use Proflow to run a standardized project workflow from requirement discovery through planning, implementation, and specification documentation. It is especially suited to agent-assisted development work that needs consistent document paths, unique requirement IDs, stage status, and execution logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify code and create repository-local planning documents, logs, status markers, and .gitignore entries.

Mitigation: Use explicit proflow commands, review generated or modified files before committing, and keep repository status checks in the workflow.

Risk: Custom requirement IDs are passed to helper scripts that create and track project artifacts.

Mitigation: Avoid unusual custom IDs and review the generated filenames and status entries before relying on them.

Risk: The skill depends on the openspec and superpowers skills for major workflow phases.

Mitigation: Install and review those dependency skills before running full, brainstorm, plan, execute, or spec workflows.

## Reference(s):

- [Proflow on ClawHub](https://clawhub.ai/luis1232023/skills/proflow)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documents, repository-local status files, log files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes project artifacts under docs/ and stage status under .opencode/status/proflow when its workflows are executed.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
