## Description: <br>
Mx Search uses Eastmoney Miaoxiang search to retrieve current financial information such as news, announcements, research reports, policy items, trading rules, event details, and impact analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessecq1995](https://clawhub.ai/user/jessecq1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts, developers, and agents use Mx Search to retrieve timely financial news, announcements, research reports, policy items, trading rules, and event information from Eastmoney Miaoxiang for review or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial search queries and API key use are sent to Eastmoney Miaoxiang. <br>
Mitigation: Install only if you trust Eastmoney/Miaoxiang, set MX_APIKEY in a trusted environment, and avoid including sensitive non-query data in prompts. <br>
Risk: Search results are saved locally as text and raw JSON files. <br>
Mitigation: Direct output to a dedicated workspace directory and review generated files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jessecq1995/mx-search-jesse) <br>
- [Eastmoney Miaoxiang news search API](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [Terminal text plus saved .txt and .json files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY; saves extracted text and raw JSON using an mx_search_ filename prefix.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
