## Description:

Use when the user asks to look up, search, or manage Google Contacts and the broader People API (Workspace directory). Triggers for contact lookups by name/email/phone, Workspace user search, profile fields, manager/reports relations, or any People API query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT

## Use Case:

Developers and users use this skill to find and manage personal Google Contacts and to look up profiles and relationships in a Google Workspace directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that Google authorization may request overly broad access.

Mitigation: Wait until authorization is limited to Contacts, and review each Google consent request before granting only the access intended.

Risk: The security assessment reports a contact deletion path that bypasses the CLI confirmation gate.

Mitigation: Avoid contact deletion until the confirmation issue is addressed; review the target contacts and obtain explicit confirmation before deletion.

Risk: The security assessment covered 12 of 14 components and only partially analyzed two files, so it cannot establish that the skill is safe.

Mitigation: Review the remaining and partially analyzed components before installation or use.

## Reference(s):

- [Project repository (listed in skill documentation)](https://github.com/chrischall/gogcli-mcp)
- [gogcli command-line tool](https://github.com/openclaw/gogcli)
- [Model Context Protocol](https://modelcontextprotocol.io)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Contact and directory results, including raw JSON and vCard exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the authorized Google account and its Contacts and People API access.]

## Skill Version(s):

4.12.0 (source: release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
