## Description:

AI-agent-friendly Hologres CLI with safety guardrails and structured JSON output for database operations, schema inspection, SQL execution, data import/export, Dynamic Table lifecycle management, and GUC parameter management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbingyu](https://clawhub.ai/user/wenbingyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data platform engineers use this skill to install and operate the Hologres CLI for database inspection, SQL execution, data import/export, Dynamic Table lifecycle management, AI/volume/model commands, and safer automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs external CLI code and can read or change production Hologres databases.

Mitigation: Install in an isolated environment, prefer a pinned and verified hologres-cli release, use least-privilege short-lived credentials, and require human review before writes, truncates, drops, GUC changes, or model registration.

Risk: The skill can export data to local files, upload local files to OSS or AI services, store credentials locally, and open downloaded files with local applications.

Mitigation: Keep masking enabled unless explicitly needed, review file upload/download and volume view actions before execution, and avoid profiles with broad credential scope.

## Reference(s):

- [Hologres CLI Command Reference](references/commands.md)
- [Hologres CLI Safety Features](references/safety-features.md)
- [Hologres CLI AI, Volume, and Model Commands](references/ai-volume-model.md)
- [ClawHub skill release page](https://clawhub.ai/wenbingyu/skills/hologres-cli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with command examples and JSON output patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run and confirmation guidance for destructive database, model, and file operations.]

## Skill Version(s):

0.2.0 (source: server release metadata, target metadata, VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
