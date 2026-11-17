## Description:

Use Zixflow to read, create, update, and delete workspace data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Zixflow collections, lists, records, and workspace members, and to create, update, or delete collection records and list entries. Confirm the intended payload and target before any write or deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may silently install or refresh other agent skills during startup.

Mitigation: Review the CLI's automatic installation behavior. Set OO_SKILLS_SYNC_DISABLED=1 for every invocation if it applies, and limit the connected Zixflow account's permissions.

Risk: Create, update, and delete actions can change or remove Zixflow data.

Mitigation: Confirm the exact payload and target before writes or deletions, and retain confirmations for changes and deletions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Zixflow API documentation](https://docs.zixflow.com/api-reference/introduction)
- [Zixflow](https://zixflow.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON payloads and results with Markdown operating guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
