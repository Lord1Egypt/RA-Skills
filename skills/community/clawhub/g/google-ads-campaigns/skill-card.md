## Description: <br>
Inspect Google Ads accounts and campaigns, run GAQL reports, and coordinate campaign or audience changes with confirmation via the Google Ads API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, and developers use this skill to inspect Google Ads customers and campaigns, run GAQL performance reports, and coordinate campaign, ad group, audience, or customer-list changes after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected Google account can expose Google Ads accounts available to that account. <br>
Mitigation: Connect only the intended Google account and verify the active Google Ads integration before use. <br>
Risk: Campaign, ad group, audience, or customer-list writes can change advertising configuration or spend. <br>
Mitigation: Preview each write operation and require explicit user confirmation before execution. <br>


## Reference(s): <br>
- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start) <br>
- [Google Ads API Reference](https://developers.google.com/google-ads/api/reference/rpc) <br>
- [GAQL Query Builder](https://developers.google.com/google-ads/api/docs/query/overview) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/google-ads-campaigns) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ClawLink-mediated Google Ads tool calls; write operations require preview and explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
