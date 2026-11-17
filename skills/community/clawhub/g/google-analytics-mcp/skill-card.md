## Description:

Query Google Analytics 4 data, including reports, funnels, realtime data, and property details, via the GA MCP server using per-workspace service account credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vittor1o](https://clawhub.ai/user/vittor1o)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to let an agent query Google Analytics 4 accounts, properties, reports, funnels, realtime data, and related property information from a workspace-scoped service account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper runs unpinned external code while service-account credentials are available.

Mitigation: Use a pinned, reviewed dependency version or a locked local install before running the helper.

Risk: The helper uses service-account credentials that could expose Google Analytics data if mishandled.

Mitigation: Keep credentials out of source control, isolate workspaces, grant only the minimum GA property Viewer role, and rotate keys if exposed.

Risk: The scanner reported unsafe path handling in the helper.

Mitigation: Review the helper before installation and run it only in trusted, isolated workspaces.

## Reference(s):

- [Google Analytics MCP server](https://github.com/googleanalytics/google-analytics-mcp)
- [Google Analytics Skill Setup Guide](references/setup.md)
- [Google Analytics Admin API](https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com)
- [Google Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include GA4 query results returned by the underlying MCP server.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
