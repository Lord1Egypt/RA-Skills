## Description: <br>
Query Google Search Console for SEO data, including search queries, top pages, CTR opportunities, URL inspection, and sitemaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, SEO analysts, and site owners use this skill to query Search Console properties, review search analytics, inspect indexing status, and identify low-CTR optimization opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OAuth setup helper prints the client ID, client secret, and refresh token after authentication. <br>
Mitigation: Run the helper in a private local terminal, avoid sharing the output in chats or logs, and store credentials in a protected secret store or private environment file. <br>
Risk: Exposed OAuth credentials could allow read-only access to Search Console properties available to the account. <br>
Mitigation: Use the documented read-only scope, limit account access to required properties, and revoke or rotate the refresh token if it is exposed. <br>


## Reference(s): <br>
- [Google Search Console documentation](https://developers.google.com/webmaster-tools) <br>
- [ClawHub skill page](https://clawhub.ai/jdrhyne/gsc) <br>
- [Publisher profile](https://clawhub.ai/user/jdrhyne) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON or tabular command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and Google OAuth environment variables for read-only Search Console access.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
