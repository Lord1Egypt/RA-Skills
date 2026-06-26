## Description: <br>
Set up AI-powered Gmail monitoring in OpenClaw that watches a Gmail inbox through Google Pub/Sub, classifies messages with an LLM, and sends important email alerts to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanaco666](https://clawhub.ai/user/nanaco666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure a Gmail watcher that sends important inbox notifications to Telegram. It is also useful for reconfiguration and troubleshooting when email alerts are not arriving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email-derived snippets and summaries may be sent to external LLM services and Telegram. <br>
Mitigation: Use a dedicated or clearly selected Gmail account, secure API keys and OpenClaw configuration, verify the Telegram chat ID, and enable LLM classification only for inboxes where third-party processing is acceptable. <br>
Risk: The install step may fetch code whose tag contents do not match the reviewed artifact. <br>
Mitigation: Confirm the referenced GitHub tag contents match the reviewed artifact before installing or publishing the release. <br>
Risk: Gmail watch and Google Pub/Sub resources can continue to exist after the plugin is removed. <br>
Mitigation: Plan cleanup of Gmail watch state, Pub/Sub topics and subscriptions, Google credentials, and related Google Cloud resources when uninstalling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nanaco666/openclaw-mail-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/nanaco666) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [gog Gmail CLI](https://gogcli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command blocks and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and troubleshooting instructions; does not create files directly.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata; artifact frontmatter and package metadata report 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
