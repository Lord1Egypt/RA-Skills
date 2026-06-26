## Description: <br>
Guides agents through selecting, configuring, validating, and monitoring NodeMaven residential or mobile proxies for account workflows, automation, and scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vkprosinnm](https://clawhub.ai/user/vkprosinnm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route a proxy workflow from account status and API-key validation through geo-targeting, access setup, tool configuration, and usage monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to handle NodeMaven API keys, proxy credentials, and sub-user passwords. <br>
Mitigation: Mask secrets in conversation, keep credentials in local environment variables or outbound authorization headers, avoid persisting proxy passwords or full proxy URLs, and rotate credentials if exposed. <br>
Risk: Proxy guidance can be misused for unauthorized scraping, ban evasion, account farming, or platform-abuse automation. <br>
Mitigation: Use the skill only for authorized workflows, require explicit user approval for purchases and account or proxy mutations, and warn users about logged-in high-volume automation risks. <br>
Risk: Incorrect proxy configuration can cause account instability, geo mismatch, rate limits, or unexpected traffic usage. <br>
Mitigation: Validate API keys, resolve location codes through the NodeMaven API, keep account geo and session strategy consistent, and monitor statistics endpoints after setup. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/vkprosinnm/nodemaven-premium-proxy) <br>
- [Publisher profile](https://clawhub.ai/user/vkprosinnm) <br>
- [NodeMaven API Swagger documentation](https://dashboard.nodemaven.com/documentation/v2/swagger/) <br>
- [NodeMaven API base URL](https://api.nodemaven.com) <br>
- [NodeMaven registration](https://dashboard.nodemaven.com/accounts/signup/?utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill) <br>
- [NodeMaven API key page](https://dashboard.nodemaven.com/user-profile?tab=API_KEY&utm_source=ai_agent&utm_medium=agent_skill&utm_campaign=nodemaven_proxy_skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include masked credential handling guidance, proxy URL templates, and monitoring steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
