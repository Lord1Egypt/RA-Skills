## Description: <br>
Mailchimp Marketing API integration with managed OAuth for accessing audiences, campaigns, templates, automations, reports, and subscriber management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Mailchimp email marketing workflows through Maton-managed OAuth, including audiences, subscribers, campaigns, templates, automations, reports, and batch operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill brokers access to a connected Mailchimp account through Maton and requires a sensitive MATON_API_KEY. <br>
Mitigation: Install only when Maton is trusted for Mailchimp access, keep MATON_API_KEY secret, and use only the intended active OAuth connection. <br>
Risk: Actions can affect audiences, campaigns, subscribers, templates, automations, reports, and batch operations in Mailchimp. <br>
Mitigation: Before approving writes, verify the exact connection, audience, campaign, subscriber, recipient count, timing, and intended effect. <br>
Risk: Destructive or high-impact operations include permanent subscriber deletion, campaign sending or scheduling, automation starts, and batch changes. <br>
Mitigation: Require explicit user approval for create, update, delete, send, schedule, automation, and batch operations, with the target resource and effect stated before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/mailchimp) <br>
- [Mailchimp Marketing API Documentation](https://mailchimp.com/developer/marketing/) <br>
- [Mailchimp Marketing API Reference](https://mailchimp.com/developer/marketing/api/) <br>
- [Mailchimp Marketing API Quick Start Guide](https://mailchimp.com/developer/marketing/guides/quick-start/) <br>
- [Mailchimp Developer Release Notes](https://mailchimp.com/developer/release-notes/) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Mailchimp OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
