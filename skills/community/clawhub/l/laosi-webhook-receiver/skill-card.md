## Description: <br>
Receives and processes webhook events with local logging, event filtering, retry-oriented handling examples, and GitHub-style signature verification guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to add local webhook receiving, event persistence, handler dispatch, and signature-checking patterns to integrations such as CI/CD, payment callbacks, monitoring alerts, and chat events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook headers and payload-derived event data may be written to local webhook_logs.json. <br>
Mitigation: Redact authorization, signature, and other sensitive headers before logging, and set an explicit retention policy for stored events. <br>
Risk: A local HTTP listener can expose webhook handling surfaces if bound or tunneled beyond the intended environment. <br>
Mitigation: Confirm listener binding, firewall, tunnel, and authentication settings before using the skill with production or sensitive webhook sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-webhook-receiver) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code snippets and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local webhook logging behavior and signature verification examples.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence, SKILL.md frontmatter, hub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
