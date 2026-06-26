## Description: <br>
Query Google Analytics 4 data, including reports, funnels, realtime metrics, and property details, via the GA MCP server using per-workspace service account credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vittor1o](https://clawhub.ai/user/vittor1o) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to query GA4 reports, funnels, realtime data, and property details from a workspace with its own Google service account credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace service account JSON can expose read access to GA4 properties if committed, shared, or stored with broad file access. <br>
Mitigation: Use a least-privilege service account with Viewer access only, keep credentials out of source control and backups where possible, restrict file permissions, and rotate or revoke the JSON key if it may have been exposed. <br>
Risk: The skill can read GA4 data for every property granted to the configured service account. <br>
Mitigation: Install only in workspaces where GA4 read access is appropriate, and scope each workspace service account to the intended properties. <br>


## Reference(s): <br>
- [Google Analytics Skill Setup Guide](references/setup.md) <br>
- [Google Analytics MCP server](https://github.com/googleanalytics/google-analytics-mcp) <br>
- [Google Analytics Admin API](https://console.cloud.google.com/apis/library/analyticsadmin.googleapis.com) <br>
- [Google Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com) <br>
- [Google Cloud IAM Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses workspace-local Google service account JSON and optional ga-config.json; query results depend on GA4 permissions and the selected MCP tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
