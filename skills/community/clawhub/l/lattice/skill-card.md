## Description:

Initialize and manage Lattice organizations, a file-based operating system for AI agent teams that supports stable long-running development through an 8-phase pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnf6682](https://clawhub.ai/user/cnf6682)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to scaffold persistent organization and project files for multi-agent work, configure an 8-phase project pipeline, and maintain status across long-running iterations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring autonomous workflow can continue modifying project files, spawning agents, and running generated test commands after setup.

Mitigation: Enable it only for intended repositories and confirm the repo path, ORG path, schedule, model budget, notification target, and stop or delete procedure before enabling cron.

Risk: Generated TASKS.md test commands may be unsafe or inappropriate for the current repository.

Mitigation: Review generated commands before execution or constrain allowed commands with an allowlist.

Risk: Scheduled agents may access unrelated files or secrets if granted broad filesystem or credential access.

Mitigation: Run with least-privilege sandbox permissions and avoid exposing secrets, home directories, credential stores, or unrelated repositories.

## Reference(s):

- [Lattice Skill Page](https://clawhub.ai/cnf6682/skills/lattice)
- [Pipeline Framework Design](artifact/templates/ORG/PROJECTS/pipeline-framework/DESIGN.md)
- [Pipeline Guide](artifact/templates/ORG/PIPELINE_GUIDE.md)
- [Pipeline State Template](artifact/templates/ORG/PROJECTS/pipeline-framework/templates/PIPELINE_STATE.template.json)
- [Orchestrator Prompt Template](artifact/templates/ORG/PROJECTS/pipeline-framework/templates/ORCHESTRATOR_PROMPT.template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration files, shell command suggestions, and file scaffolding instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent ORG and project files, pipeline status artifacts, model and agent role configuration, and optional cron orchestration guidance.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
