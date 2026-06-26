## Description: <br>
Provides Ghost CMS development guidance for installation, theme creation with Handlebars, Ghost CLI usage, API integration, GScan validation, routing, publishing, deployment, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[themeix](https://clawhub.ai/user/themeix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to plan, build, validate, manage, and deploy Ghost CMS sites and themes. It also helps with Ghost Content API and Admin API usage, including examples for publishing workflows and site management tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ghost Admin API examples can create, edit, publish, delete, upload, or activate site resources if applied to a live instance. <br>
Mitigation: Require explicit approval before edits, deletes, member or webhook changes, image uploads, theme activation, production installs, updates, or deployments. <br>
Risk: Admin API keys, staff tokens, and integration credentials can grant sensitive site-management access. <br>
Mitigation: Treat keys as secrets, avoid exposing them in client-side code, and prefer environment variables or secure secret storage. <br>
Risk: Theme and content changes can affect production site availability, appearance, or published content. <br>
Mitigation: Prefer local or staging Ghost instances, validate themes with GScan, and back up content and themes before applying changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/themeix/openclaw-ghost-cms) <br>
- [Ghost Docs](https://ghost.org/docs/) <br>
- [Ghost Theme Development](https://ghost.org/docs/themes/) <br>
- [Ghost CLI](https://ghost.org/docs/ghost-cli/) <br>
- [Ghost Content API](https://ghost.org/docs/content-api/) <br>
- [Ghost Admin API](https://ghost.org/docs/admin-api/) <br>
- [GScan](https://gscan.ghost.org/) <br>
- [Complete Ghost API Reference](https://docs.ghost.org/llms-full.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, JSON, YAML, JavaScript, Python, and Handlebars examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands, configuration changes, API calls, theme files, and operational steps for Ghost CMS workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
