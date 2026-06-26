## Description: <br>
Hostinger API integration via managed credentials for inspecting domains, DNS records, VPS instances, websites, subscriptions, and hosting account data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to query and manage Hostinger hosting resources through ClawLink-managed credentials. It supports account discovery, DNS and domain workflows, website and VPS inspection, and confirmed account-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting a Hostinger account through ClawLink grants access to account resources and managed credentials. <br>
Mitigation: Install only when comfortable with the ClawLink connection model and verify the Hostinger connection before using account tools. <br>
Risk: DNS, VPS, website, domain, subscription, or billing-related changes can affect live services and account resources. <br>
Mitigation: Review previews carefully and require explicit user confirmation before any account-changing action. <br>
Risk: Tool availability can vary with the connected Hostinger account and live ClawLink catalog. <br>
Mitigation: List integrations and tools first, treat the returned catalog as authoritative, and use tool descriptions before unfamiliar or ambiguous calls. <br>


## Reference(s): <br>
- [Hostinger API Documentation](https://developers.hostinger.com/) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=hostinger-hosting) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live Hostinger tool catalog as the source of truth and requires previews plus explicit confirmation for write operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
