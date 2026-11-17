## Description:

Notion API for creating and managing pages, databases, blocks, relations, rollups, and multi-workspace profiles via the notioncli CLI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordancoin](https://clawhub.ai/user/jordancoin)

### License/Terms of Use:


## Use Case:

Developers, operators, and AI agents use this skill to interact with Notion workspaces from the terminal, including querying databases, managing pages and blocks, updating relations and rollups, uploading files, and working across multiple workspace profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete Notion workspace content.

Mitigation: Use a least-privilege Notion integration shared only with intended pages and databases, and confirm uniquely identified targets before destructive commands.

Risk: The install path uses an unpinned global npm package with inconsistent package naming in the artifact.

Mitigation: Verify the npm package identity and version manually before installing or executing the CLI.

Risk: The skill persists and uses a Notion API credential.

Mitigation: Protect NOTION_API_KEY, avoid exposing it through shell history or process logs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jordancoin/skills/notioncli)
- [Notion CLI Homepage](https://github.com/JordanCoin/notioncli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to install and invoke notioncli, configure NOTION_API_KEY, and request JSON, CSV, YAML, or table output from the CLI.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
