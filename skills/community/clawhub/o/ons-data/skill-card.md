## Description:

This skill helps agents query ONS-style dataset metadata and observations through a Xiaobenyang MCP proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent list, search, and retrieve ONS-style dataset information, observations, and latest data with supplied filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the skill is presented as a no-key ONS connector but actually requires, stores, and sends a Xiaobenyang API key through a third-party proxy.

Mitigation: Review the third-party service, credential storage, retention, and deletion process before installation, and only use the skill if that proxy and plaintext workspace key storage are acceptable.

Risk: The skill behavior depends on a third-party proxy rather than a direct official ONS API connection.

Mitigation: Prefer a corrected package that directly calls the official ONS API or require clear disclosure of the third-party service path before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/ons-data)
- [Xiaobenyang service](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or structured text summarizing JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require an XBY API key stored in the workspace environment before use.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
