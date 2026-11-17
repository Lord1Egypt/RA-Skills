## Description:

Structured memory system for AI agents with a local markdown vault and Notion sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kitakitsune0x](https://clawhub.ai/user/kitakitsune0x)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Memoria to store, search, retrieve, and sync structured memories across sessions, including decisions, facts, preferences, lessons, commitments, relationships, and projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent recording of conversation details, which can capture sensitive personal or third-party information.

Mitigation: Review memory capture before use, remove proactive capture guidance when inappropriate, and avoid storing secrets, health data, or third-party personal details.

Risk: Notion sync can copy local memories to a user-configured external workspace.

Mitigation: Keep Notion auto-sync disabled unless needed, use explicit sync choices, and verify workspace access before syncing.

Risk: Notion tokens entered on the command line may be exposed through shell history or process logs.

Mitigation: Rotate any token entered this way and prefer safer credential handling before deployment.

Risk: Security evidence reports a vault path validation issue.

Mitigation: Fix path validation before deployment and restrict the vault to intended directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kitakitsune0x/skills/memoria)
- [Notion integrations](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands and structured memory content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local markdown vault files and optionally synchronize them with a user-configured Notion workspace.]

## Skill Version(s):

0.2.1 (source: server release metadata; package.json is 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
