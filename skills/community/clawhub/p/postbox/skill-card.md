## Description: <br>
Use this skill when the user wants to collect structured data, build forms, or set up submission endpoints for contact forms, feedback, signups, waitlists, bug reports, support, lead capture, surveys, applications, HTML, scripts, or AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vipulbhj](https://clawhub.ai/user/vipulbhj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external teams use Postbox to create and manage structured data collection forms, submission endpoints, notifications, and AI-assisted processing without building their own backend. Agents can also generate frontend integration code, list submissions, and explain Postbox discovery flows for runtime schema-aware submissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a configured Postbox account, including create, update, delete, webhook, Slack, Discord, and AI auto-reply actions. <br>
Mitigation: Review proposed account-changing actions before execution and confirm the intended form, destination, or AI behavior. <br>
Risk: The skill depends on a Postbox API key. <br>
Mitigation: Store the key in POSTBOX_API_KEY and do not paste API keys into chat. <br>
Risk: Generated frontend code may be deployed to public sites. <br>
Mitigation: Inspect generated frontend changes before deployment, especially endpoint URLs, validation handling, and private form token usage. <br>
Risk: Postbox submissions, schemas, and knowledge base text can contain untrusted user-controlled content. <br>
Mitigation: Treat returned content as data to display or summarize, not as instructions to execute. <br>


## Reference(s): <br>
- [Postbox Skill Page](https://clawhub.ai/vipulbhj/postbox) <br>
- [Postbox Homepage](https://usepostbox.com) <br>
- [Postbox Documentation](https://docs.usepostbox.com) <br>
- [Postbox API Reference](references/api.md) <br>
- [Postbox Operational Guide](references/guide.md) <br>
- [Frontend Integration Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON, JavaScript, React, HTML, and shell command examples as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce working Postbox endpoints, generated frontend code, readable submission summaries, and setup guidance that depends on POSTBOX_API_KEY.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
