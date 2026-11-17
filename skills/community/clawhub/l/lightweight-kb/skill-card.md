## Description:

Lightweight Knowledge Base provides a Chinese-language local knowledge base and task-management system using hybrid JSON and Markdown storage for user profiles, task rhythms, knowledge indexing, and daily evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamtie](https://clawhub.ai/user/williamtie)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to maintain a local personal knowledge base, query user-profile and task-rhythm data, and run recurring review or daily-evolution workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists user profile, preferences, task rhythm, and knowledge-index files locally.

Mitigation: Install only where local profile persistence is expected, review stored JSON files before sharing a workspace, and delete or redact sensitive profile fields when they are no longer needed.

Risk: The documented source <(jq ...) shell template can execute values derived from modified JSON as shell code.

Mitigation: Do not use that template with untrusted or user-editable JSON; inspect task data first and prefer explicit jq reads into ordinary variables.

Risk: Query commands without keywords can display the full profile or task schedule on screen.

Mitigation: Use specific query terms when possible and avoid running full-profile or full-task queries in shared logs, demos, or screen-sharing sessions.

Risk: Automated and deep-dialogue tasks can collect or refresh profile information over time.

Mitigation: Review the enabled tasks before use and disable scheduled profile-collection tasks unless the user has explicitly opted in.

## Reference(s):

- [Communication Guide](artifact/references/communication.md)
- [Task Execution Guide](artifact/references/task_guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/williamtie/skills/lightweight-kb)
- [ClawHub Publisher Profile](https://clawhub.ai/user/williamtie)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file outputs may include profile, task-rhythm, knowledge-index, memory-node, report, and temporary-cache files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
