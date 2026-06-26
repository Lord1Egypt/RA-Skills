## Description: <br>
Hivebrite Admin API CLI covering users, companies, events, groups, donations, memberships, emailings, mentoring, news, projects, media center, forums, and more with OAuth2 or bearer token authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdelkrim](https://clawhub.ai/user/abdelkrim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to let an agent run Hivebrite Admin API operations from a Node.js CLI, including reading records and managing users, groups, events, memberships, content, email campaigns, payments, donations, mentoring, and network settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real changes to a Hivebrite community when supplied admin credentials. <br>
Mitigation: Use a least-privileged token or dedicated admin user and require human review before state-changing operations. <br>
Risk: OAuth credentials, bearer tokens, and cached refresh tokens can expose administrative access if leaked. <br>
Mitigation: Keep .env files and the cached OAuth token file out of version control and rotate credentials if exposure is suspected. <br>
Risk: Send, notify, approval, admin, payment, donation, membership, and content commands can affect users or transactions. <br>
Mitigation: Review command arguments and target records before execution, especially for bulk or irreversible actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abdelkrim/hivebrite-by-altf1be) <br>
- [Declared source homepage](https://github.com/ALT-F1-OpenClaw/openclaw-skill-hivebrite-by-altf1be) <br>
- [Publisher profile](https://clawhub.ai/user/abdelkrim) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return Hivebrite API data, status messages, or errors depending on the invoked operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, _meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
