## Description: <br>
Monitor competitor product prices across Shopee, Lazada, Amazon, and other e-commerce platforms with automated tracking, alerts, reports, and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers, dropshippers, and small business owners use this skill to track competitor product URLs, compare prices over time, receive threshold alerts, and generate pricing reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Competitor URLs, alert rules, price history, and generated reports may reveal sensitive product strategy if stored or shared unexpectedly. <br>
Mitigation: Keep the workspace access-controlled, review generated files before sharing, and avoid entering product strategy data that should not be persisted. <br>
Risk: Recurring scans can run automatically after setup and may continue collecting price data or triggering alerts. <br>
Mitigation: Confirm the cron schedule, scan frequency, and tracked product list before enabling automation, and remove schedules that are no longer needed. <br>
Risk: Alerts sent through Telegram, email, Discord, or similar channels may disclose pricing intelligence to third-party services. <br>
Mitigation: Review the destination for each alert channel and send sensitive pricing information only through channels approved for that data. <br>


## Reference(s): <br>
- [GTS Ecommerce Price Monitor ClawHub Release](https://clawhub.ai/ericlooi504/gts-ecommerce-price-monitor) <br>
- [Advanced Configuration](references/CONFIG.md) <br>
- [Platform-Specific Notes](references/PLATFORMS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain-text guidance with inline shell commands, JSON/JSONL tracking data, and optional CSV reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local product, alert, price-history, and report files in the workspace when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
