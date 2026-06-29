## Description: <br>
Ora社媒主页搜索专家 helps agents find LinkedIn, Facebook, Twitter/X, and Instagram homepages by keyword or by company/domain reverse lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oraagent](https://clawhub.ai/user/oraagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sales or research agents use this skill to locate company social media homepages and lead context from keywords, company names, or domains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords, company names, and domains are sent to api.topeasychina.com. <br>
Mitigation: Use the skill only with business data that is appropriate to send to that service. <br>
Risk: The skill reads OraAgent.key as an AuthToken and logs token presence. <br>
Mitigation: Treat OraAgent.key as a secret, avoid placing unrelated credentials there, and reduce token logging before sensitive use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oraagent/ora-sns-pro) <br>
- [Keyword search API endpoint](https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaQuery) <br>
- [Domain search API endpoint](https://api.topeasychina.com:9443/DomainData/api/skill/socialMediaDomainQuery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown result lists with social profile links, source website links, summaries, and usage-status footer text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and sends search keywords, company names, or domains to fixed OraAgent API endpoints.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
