## Description: <br>
Confluence REST API integration via curl - lightweight solution without Python dependencies. Supports search, page operations, and file attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukaizj](https://clawhub.ai/user/lukaizj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to search Confluence, retrieve pages, create or update wiki content, list spaces, and upload attachments through the Confluence REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Confluence content using the configured account. <br>
Mitigation: Install only for intended Confluence use, prefer a dedicated API token or service account with limited space permissions, and review create, update, and attach actions before execution. <br>
Risk: Incorrect Confluence endpoint or credential configuration could expose requests to the wrong instance or account boundary. <br>
Mitigation: Verify that CONFLUENCE_URL uses HTTPS and points to the intended Confluence instance before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lukaizj/lukaizj-confluence) <br>
- [Project homepage](https://github.com/lukaizj/confluence-integration-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command guidance for Confluence REST operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CONFLUENCE_URL, CONFLUENCE_USER, and CONFLUENCE_PASS environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
