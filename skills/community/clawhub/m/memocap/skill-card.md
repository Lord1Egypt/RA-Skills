## Description:

memocap provides an agent-facing memory system for retrieval, storage, forgetting, time capsules, visualization, and user profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users can use memocap to recall prior context, store valuable decisions, preferences, tasks, emotions, and timestamps, and manage memory records through local retrieval, merge, export, capsule, visualization, and profile commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist detailed user data in a local memory store.

Mitigation: Require confirmation before storing personal or sensitive details and keep review, deletion, and purge controls available.

Risk: The skill can broadly activate on memory-related terms.

Mitigation: Narrow activation to explicit commands before routine use.

Risk: The skill runs separate local scripts from the user's home directory.

Mitigation: Verify the helper scripts' origin and integrity before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/memocap)
- [Publisher profile](https://clawhub.ai/user/fslong520)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can direct use of local memory scripts and persistent user records when the required local data directory and helper scripts are present.]

## Skill Version(s):

2.5.10 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
