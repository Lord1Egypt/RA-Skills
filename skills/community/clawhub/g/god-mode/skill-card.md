## Description:

Developer oversight and AI agent coaching. Use when viewing project status across repos, syncing GitHub data, or analyzing agents.md against commit patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infantlab](https://clawhub.ai/user/infantlab)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to track activity across configured repositories, sync GitHub project data into a local cache, and generate prompts that analyze agent instructions against commit patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository metadata, commit history, and agent-instruction files, then stores snapshots and analysis data locally.

Mitigation: Use it only with repositories you trust and keep ~/.god-mode private.

Risk: Custom agent file patterns can broaden what repository files are read for analysis.

Mitigation: Avoid analysis.agentFiles entries that use absolute paths or parent-directory components.

Risk: Generated analysis prompts and recommendations may contain sensitive repository context or suggest unsafe instruction changes.

Mitigation: Review generated prompts and recommendations before sending them to an LLM or applying them to agent instructions.

Risk: Adding the cloned scripts directory persistently to PATH can expose the shell to unreviewed command changes.

Mitigation: Prefer a temporary PATH entry unless the cloned scripts have been reviewed and are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infantlab/skills/god-mode)
- [Publisher profile](https://clawhub.ai/user/infantlab)
- [GitHub CLI documentation](https://cli.github.com/)
- [Configuration example](config.example.yaml)
- [Agent analysis prompt](prompts/agent-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON, Markdown prompts, shell commands, and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local status summaries and agent-analysis prompts; generated recommendations should be reviewed before use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
