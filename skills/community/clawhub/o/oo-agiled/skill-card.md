## Description:

Agiled (agiled.app). Use this skill for ANY Agiled request — reading, creating, updating, and deleting data. Whenever a task involves Agiled, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams can use the skill to read and manage Agiled contacts, projects, and tasks through their connected account. It guides agents to check each action's schema and obtain confirmation before writes or deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded installer code that has not been verified.

Mitigation: Preinstall a reviewed oo CLI release and require approval before local installation.

Risk: CLI startup synchronization may change other installed agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if you want to disable startup skill synchronization.

Risk: Write and delete actions change Agiled records.

Mitigation: Confirm the exact payload and effect before writes, and explicitly approve the target before deletions.

## Reference(s):

- [Agiled skill release](https://clawhub.ai/oomol/skills/oo-agiled)
- [Agiled homepage](https://agiled.app)
- [Agiled API documentation](https://my.agiled.app/developers)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Schema-guided connector requests and structured JSON responses, with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports read, create, update, and delete actions; confirm writes and explicitly approve deletions.]

## Skill Version(s):

1.0.4 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
