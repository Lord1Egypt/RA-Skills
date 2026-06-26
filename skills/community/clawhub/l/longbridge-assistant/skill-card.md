## Description: <br>
LongbridgeAssistant monitors Longbridge brokerage holdings, generates portfolio visualizations, checks price alerts, and summarizes portfolio analysis guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p3dp](https://clawhub.ai/user/p3dp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Longbridge OpenAPI credentials use this skill to inspect brokerage holdings, generate Hong Kong and U.S. portfolio charts, and receive price-alert and concentration guidance. The artifact describes monitoring and analysis only, not trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles brokerage API credentials and reads them from a local Longbridge environment file. <br>
Mitigation: Use a least-privilege or read-only Longbridge token when available, store ~/.longbridge/env with restrictive permissions, and avoid sharing credential files or logs. <br>
Risk: Generated charts and console output may expose portfolio holdings and financial account details. <br>
Mitigation: Treat generated portfolio charts and logs as sensitive financial data and avoid uploading or sharing them unless intentionally disclosed. <br>
Risk: Bundled monetization material discusses user financial data and higher-risk financial services. <br>
Mitigation: Review the monetization content and remove or constrain any data-use practices that are not acceptable for the intended deployment. <br>


## Reference(s): <br>
- [Longbridge Open Platform](https://open.longportapp.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/p3dp/longbridge-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/p3dp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Console text with setup guidance and a generated PNG portfolio chart] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Longbridge API credentials in LONGBRIDGE_APP_KEY, LONGBRIDGE_APP_SECRET, and LONGBRIDGE_ACCESS_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
