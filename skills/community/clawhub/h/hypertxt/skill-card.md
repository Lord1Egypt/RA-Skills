## Description:

Operate Hypertxt articles and Google Search Console through the Hypertxt MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[julianengel](https://clawhub.ai/user/julianengel)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams and agents use this skill to inspect Hypertxt account and project data, identify GSC-backed content opportunities, generate articles, review editorial state, export content, and create CMS drafts or live publications with explicit approvals for high-impact actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward spending article credits, changing editorial state, syncing GSC data, or publishing to connected destinations.

Mitigation: Require explicit user approval immediately before each high-impact action and report the exact project, article, destination, mode, and credit impact before proceeding.

Risk: Hypertxt API key exposure would grant account access through the configured client.

Mitigation: Never request or echo the API key; keep it in the client's environment or secret configuration as HYPERTXT_API_KEY.

Risk: Publishing or state changes could target the wrong article, project, or destination if identifiers are guessed.

Mitigation: Discover identifiers with list tools, confirm the selected resources with the user, and distinguish destination drafts from live publication.

## Reference(s):

- [Hypertxt OpenClaw setup guide](https://www.hypertxt.ai/guides/openclaw/)
- [ClawHub skill page](https://clawhub.ai/julianengel/skills/hypertxt)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration guidance]

**Output Format:** [Markdown text with tool-use decisions, approval prompts, and workflow status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Hypertxt MCP server and HYPERTXT_API_KEY stored in the client environment or secret configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
