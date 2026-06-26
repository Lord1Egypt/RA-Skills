## Description: <br>
Mailtarget Email lets agents send transactional and marketing email through the Mailtarget API and manage templates, sending domains, API keys, and sub-accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masasdani](https://clawhub.ai/user/masasdani) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and operators use this skill to let an agent prepare and send Mailtarget emails, manage reusable templates, configure sending domains, and administer related account resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority over live Mailtarget email, account, tracking, API-key, sub-account, and optional DNS-changing operations. <br>
Mitigation: Install only for real Mailtarget account operations, use narrowly scoped Mailtarget and Cloudflare credentials, and require explicit approval before sending campaigns, enabling tracking, bypassing unsubscribe preferences, changing DNS, deleting resources, or managing API keys and sub-accounts. <br>
Risk: Email recipients, content, attachments, and DNS records may be incorrect or inappropriate if executed without review. <br>
Mitigation: Review all recipients, content, attachments, and DNS records before execution. <br>


## Reference(s): <br>
- [Mailtarget API Reference](references/api.md) <br>
- [Getting Started with Mailtarget + OpenClaw](references/getting-started.md) <br>
- [Mailtarget API Docs](https://developer.mailtarget.co) <br>
- [Mailtarget Dashboard](https://app.mailtarget.co) <br>
- [ClawHub Skill Page](https://clawhub.ai/masasdani/mailtarget-email) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Mailtarget API requests that send email, alter templates, manage domains, administer API keys, or manage sub-accounts.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
