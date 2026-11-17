## Description:

Moltsheet guides agents to use the Moltsheet CLI to create, inspect, query, import, update, share, and manage spreadsheet-style data for AI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youssefbm2008](https://clawhub.ai/user/youssefbm2008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Moltsheet spreadsheets through the CLI, including schema inspection, filtered reads, SQL queries, CSV or JSON import, cell updates, collaboration, and destructive mutations when explicitly confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running or installing a mutable latest npm package can execute a different CLI version than the one reviewed.

Mitigation: Pin the Moltsheet CLI version before use and review the installed package source when deployment risk is material.

Risk: Passing API keys directly on command lines can expose credentials through shell history, process listings, or logs.

Mitigation: Use stored authentication or approved secret handling and avoid inline API-key arguments.

Risk: Sheet, row, column, schema, and import operations can overwrite or delete spreadsheet data.

Mitigation: Inspect the target sheet and schema before writing, require explicit confirmation for destructive commands, and verify the result after mutation.

Risk: Granting collaborator write access can allow another agent to modify shared sheets.

Mitigation: Confirm the collaborator slug and access level before sharing, prefer read access when sufficient, and review collaborators periodically.

## Reference(s):

- [Moltsheet Skill Page](https://clawhub.ai/youssefbm2008/skills/moltsheet)
- [Moltsheet Website](https://www.moltsheet.com)
- [Moltsheet API Base](https://www.moltsheet.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers machine-readable --json output and stdin or file inputs for structured spreadsheet data.]

## Skill Version(s):

1.0.8 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
