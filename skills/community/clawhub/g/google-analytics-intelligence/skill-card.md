## Description: <br>
Analyze GA4 data, detect traffic anomalies, and generate actionable growth recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ncreighton](https://clawhub.ai/user/ncreighton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, SaaS founders, e-commerce managers, and growth analysts use this skill to analyze Google Analytics 4 metrics, detect unusual traffic or conversion changes, generate reports, and produce growth recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access Google Analytics metrics that reveal business performance, user behavior, revenue, or campaign details. <br>
Mitigation: Use least-privileged Google credentials, limit the GA4 property scope, and run the skill only in approved environments. <br>
Risk: Configured Slack webhooks can post analytics summaries or alerts to shared channels. <br>
Mitigation: Send reports only to private approved channels, protect webhook URLs, and rotate them if exposed. <br>
Risk: API keys and webhook URLs are required for normal operation and could be exposed if stored in shared files or transcripts. <br>
Mitigation: Keep credentials out of shared files, use secret storage where available, and rotate credentials after any suspected exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ncreighton/google-analytics-intelligence) <br>
- [Publisher profile](https://clawhub.ai/user/ncreighton) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Google Analytics](https://analytics.google.com) <br>
- [Slack API](https://api.slack.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and recommendations with inline configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include analytics summaries, anomaly alerts, growth recommendations, report templates, and Slack-ready messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
