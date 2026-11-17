## Description:

Long-running agent workflow automation. Initialize project scaffolding, manage feature lists, track progress across sessions, and orchestrate coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenkangwei](https://clawhub.ai/user/wenkangwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to initialize shared project state, break work into testable features, run one-feature coding sessions, and preserve handoff notes across long-running agent projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local execution and git mutation workflows may change project files or commits in ways the user did not intend.

Mitigation: Install only in a disposable or trusted workspace, inspect git status and staged diffs before committing, and avoid git add -A when secrets or unrelated files may be present.

Risk: Project startup scripts can run local commands defined in the workspace.

Mitigation: Review init.sh before every run and avoid running the harness from untrusted repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenkangwei/skills/long-running-agent-harness)
- [Anthropic engineering blog: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Architecture overview](docs/architecture.md)
- [Session sequence diagram](docs/sequence.md)
- [File and component relationships](docs/file-flow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and project tracking files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompts and local project files for feature tracking, progress logs, initialization scripts, and harness configuration.]

## Skill Version(s):

1.0.0 (source: server release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
