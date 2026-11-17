## Description:

Multi-Agent Memory Optimizer manages private and public memory spaces for OpenClaw agents, generates daily summaries, and enables cross-agent knowledge retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2720480371](https://clawhub.ai/user/2720480371)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to organize agent memory into private, medium-term, long-term, and shared public spaces. It supports daily summary generation, optional publication of selected memory, and search across public or private memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private memory can be published to a public shared space without the documented confirmation behavior.

Mitigation: Keep upload.require_upload_confirm enabled, review generated summaries before upload, and use dry-run or manual approval before trusting the skill with private memory.

Risk: Unsafe path and shell handling could affect files outside the intended memory workspace.

Mitigation: Validate agent IDs and titles before file operations, constrain configured memory paths to the intended workspace, and replace shell-based workflow execution with direct function calls or shell-free subprocesses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2720480371/skills/memory-optimizer-base)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown files, JSON configuration, terminal status text, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and searches filesystem-backed memory summaries; publication to public memory should be reviewed before use.]

## Skill Version(s):

0.2.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
