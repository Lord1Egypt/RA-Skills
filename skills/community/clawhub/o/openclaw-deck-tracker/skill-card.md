## Description: <br>
Track OpenClaw tasks on NextCloud Deck board. Auto-add tasks to Queue, move through states. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SkanderHelali](https://clawhub.ai/user/SkanderHelali) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to manage an OpenClaw agent's task lifecycle on a NextCloud Deck board, including task creation, progress logging, status movement, daily archiving, and completed-task export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store task details in an external NextCloud Deck instance. <br>
Mitigation: Avoid tracking secrets or private prompts and review card content before sharing or archiving it. <br>
Risk: Monitor notifications may send task status to an unintended recipient. <br>
Mitigation: Verify the configured notification target before starting background monitoring. <br>
Risk: Archive and delete commands can remove or hide task records. <br>
Mitigation: Manually review cards before running archive or delete commands. <br>
Risk: NextCloud access depends on credentials exposed to the agent environment. <br>
Mitigation: Use a limited NextCloud app password and install only when the separate deck CLI is trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SkanderHelali/openclaw-deck-tracker) <br>
- [NextCloud Deck App](https://apps.nextcloud.com/apps/deck) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output where supported] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can cause an agent to create, update, archive, delete, and export NextCloud Deck cards through a separate deck CLI.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
