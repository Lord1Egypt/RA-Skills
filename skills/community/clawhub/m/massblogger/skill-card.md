## Description: <br>
Massblogger connects an agent to a hosted MCP server for managing WordPress sites, generating content, publishing drafts, and running bulk content operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klitmose](https://clawhub.ai/user/klitmose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, site owners, and developers use this skill to manage one or more WordPress sites through Massblogger, including content creation, editing, media handling, scheduling, SEO updates, and cross-site automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted service can perform broad, persistent read/write actions across connected live WordPress sites. <br>
Mitigation: Install only if you trust Massblogger with those sites and use dedicated least-privilege WordPress accounts wherever possible. <br>
Risk: Bulk updates, cross-site operations, and automated publishing can make large or public changes quickly. <br>
Mitigation: Require dry runs before bulk or cross-site operations, review generated content before publication, and enable publish guard for sites that should not publish automatically. <br>
Risk: Long-lived MCP tokens and WordPress Application Passwords can preserve access after a workflow is no longer needed. <br>
Mitigation: Rotate or revoke the MCP token and WordPress Application Passwords when access is no longer required or if credentials may be exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/klitmose/massblogger) <br>
- [Massblogger](https://massblogger.com) <br>
- [MCP setup docs](https://massblogger.com/docs/openclaw) <br>
- [WordPress Application Passwords guide](https://massblogger.com/docs/wordpress/application-passwords) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and remote MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a hosted MCP server; agent-side output may include WordPress content drafts, site-management actions, media operations, and status summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact release notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
