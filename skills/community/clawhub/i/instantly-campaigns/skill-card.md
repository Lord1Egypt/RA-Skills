## Description: <br>
Run scalable cold email campaigns via Instantly.ai. Manage email accounts, build lead lists, create and activate multi-step outreach sequences, track analytics, and automate follow-ups with condition-based branching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to manage Instantly.ai cold email campaigns through ClawLink, including accounts, leads, sequences, analytics, webhooks, API keys, and workspace administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth tokens and sensitive credentials for a connected Instantly workspace. <br>
Mitigation: Install only if the publisher and ClawLink are trusted, and connect only the intended Instantly workspace. <br>
Risk: Write actions can change campaigns, leads, webhooks, API keys, email accounts, labels, and workspace settings. <br>
Mitigation: Confirm the exact target resource and intended effect before approving writes, especially destructive or high-impact operations. <br>
Risk: DFY account administration can expose or retrieve account-provisioning data. <br>
Mitigation: Avoid DFY password retrieval unless account-provisioning administration is specifically required. <br>
Risk: Lead enrichment, data jobs, inbox placement tests, and email sending may incur costs or hit plan and rate limits. <br>
Mitigation: Review Instantly plan limits, billing impact, and campaign readiness before running enrichment, testing, or sending workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/instantly-campaigns) <br>
- [Publisher Profile](https://clawhub.ai/user/hith3sh) <br>
- [Instantly API Documentation](https://developer.instantly.ai/) <br>
- [Instantly Warmup Guide](https://www.instantly.io/warmup) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=instantly-campaigns) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Instantly campaign, lead, account, webhook, API key, analytics, and troubleshooting guidance based on the connected workspace.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
