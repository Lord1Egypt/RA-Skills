## Description: <br>
Interface with WordPress sites through the JRB Remote Site API plugin for content management, site administration, plugin and theme management, and Fluent suite integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrbconsulting-joel](https://clawhub.ai/user/jrbconsulting-joel) <br>

### License/Terms of Use: <br>
GPL-2.0-or-later <br>


## Use Case: <br>
Developers and site operators use this skill to let an agent connect to WordPress sites running the JRB Remote Site API plugin, then perform administrative, content, media, plugin, theme, and Fluent suite tasks through authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad power to change WordPress content, media, plugins, themes, and Fluent suite data. <br>
Mitigation: Use separate least-privilege tokens per site and require explicit human confirmation before publishing, deleting, installing or updating plugins/themes, switching themes, uploading media, or accessing CRM/support customer data. <br>
Risk: API tokens could expose administrative access if copied into prompts, logs, or shared configuration. <br>
Mitigation: Store tokens outside prompts, keep them out of logs, and rotate site-specific tokens when access changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jrbconsulting-joel/jrb-remote-site-api-skill-repo) <br>
- [WordPress plugin directory: jrb-remote-site-api-for-openclaw](https://wordpress.org/plugins/jrb-remote-site-api-for-openclaw/) <br>
- [JRB Remote Site API plugin repository](https://github.com/JRBConsulting/jrb-remote-site-api-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with configuration details and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated WordPress REST API request examples using site URLs and secure tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
