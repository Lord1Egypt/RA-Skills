## Description: <br>
Track pageviews and custom events via the Plausible Events API, and query stats including top pages, top sources, countries, and realtime visitors for a self-hosted or plausible.io site. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and analytics users can use this skill to send Plausible pageview or custom-event data and retrieve site analytics from Plausible. It is useful when an agent needs scripted access to event tracking, aggregate stats, top pages, or realtime visitor counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Plausible API key can expose analytics access if copied into chat, logs, repositories, or shared command history. <br>
Mitigation: Keep PLAUSIBLE_API_KEY in the environment or a secrets manager, avoid pasting it into prompts, and rotate it if it is exposed. <br>
Risk: Tracked URLs, referrers, event names, or event properties may contain personal data, tokens, private paths, or other sensitive analytics data. <br>
Mitigation: Review event payloads before sending them and avoid including sensitive query strings, private URLs, personal data, or secret values. <br>
Risk: Using an unexpected Plausible base URL could send events or API credentials to the wrong service. <br>
Mitigation: Use only a trusted PLAUSIBLE_BASE_URL for plausible.io or a verified self-hosted instance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kryzl19/plausible-analytics-agent) <br>
- [Plausible Analytics](https://plausible.io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with bash commands; scripts return JSON or plain text from Plausible endpoints.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PLAUSIBLE_SITE_DOMAIN and PLAUSIBLE_API_KEY for stats endpoints; PLAUSIBLE_BASE_URL can target hosted or self-hosted Plausible.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
