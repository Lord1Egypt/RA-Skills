## Description:

Publish files and websites as shareable links on litehost.io and manage them through the Connect API. Use when the user asks to deploy, host, publish, share, upload, update, list, delete, archive or manage a site, file, project or custom domain on Litehost, send work to a client as one link, get a QR code for a link, or check their Litehost plan or quota.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fernandops26](https://clawhub.ai/user/fernandops26)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and people sharing work use this skill to publish websites and files through Litehost, manage hosted projects, and obtain share links, QR codes, and project status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports workspace deletion capability beyond the declared scope.

Mitigation: Review workspace deletion behavior before use and require clear user authorization before deleting a workspace.

Risk: ClawScan reports that the project deletion helper bypasses the documented confirmation gate.

Mitigation: Require explicit user confirmation immediately before project deletion and review the helper's deletion behavior before use.

Risk: The unpinned installer is a supply-chain weakness, as stated in the security guidance.

Mitigation: Use a reviewed, fixed release when installing the skill.

Risk: The security analysis is partial and does not establish that the skill is safe.

Mitigation: Review the skill and its behavior before installing or granting it access to Litehost credentials.

## Reference(s):

- [Litehost Developer Documentation](https://litehost.io/developers)
- [Litehost Connect Agent Guide](https://connect.litehost.io/llms.txt)
- [Litehost Connect MCP Endpoint](https://connect.litehost.io/mcp)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text, Configuration instructions]

**Output Format:** [Litehost API requests and responses with user-facing Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide hosted project URLs, project IDs, temporary claim links, QR code links, and project or quota status.]

## Skill Version(s):

4.2.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
