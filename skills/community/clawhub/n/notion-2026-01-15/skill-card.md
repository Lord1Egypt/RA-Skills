## Description:

Provides guidance and curl examples for using the Notion API to create, move, update, and manage pages, data sources, blocks, templates, and locks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongkukim](https://clawhub.ai/user/dongkukim)

### License/Terms of Use:


## Use Case:

Developers and workspace administrators use this skill to compose Notion API requests for page, data source, block, template, and locking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a long-lived Notion token in a local file.

Mitigation: Use a least-privilege Notion integration, share only required pages or data sources, and store the token in a keychain or with owner-only file permissions.

Risk: Examples include content-changing operations such as moving, locking, updating, and applying templates with erase_content.

Mitigation: Require explicit confirmation before running move, lock, update, or erase-content requests against a workspace.

## Reference(s):

- [Notion Developers](https://developers.notion.com)
- [Notion Integrations](https://notion.so/my-integrations)
- [ClawHub Skill Page](https://clawhub.ai/dongkukim/skills/notion-2026-01-15)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with bash and JSON curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Notion integration token and page or data source identifiers supplied by the user.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
