## Description: <br>
Generates structured Chinese-language Iran conflict situation briefs and risk-monitoring reports from news search, Jin10 flash and market data, and local ceasefire-period analysis frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinfi-codex](https://clawhub.ai/user/chinfi-codex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts and agents use this skill to assemble daily China-language geopolitical and market-risk briefings about the Iran conflict, with source credibility labels, scenario probabilities, and risk-asset implications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends news keywords, market symbols, and fetched URLs to external data services. <br>
Mitigation: Review external-service use before running and avoid submitting confidential prompts, keywords, URLs, or proprietary watchlists. <br>
Risk: The artifact includes an embedded Jin10 service token, which creates credential-hygiene and reliability risk. <br>
Mitigation: Rotate or replace embedded credentials with user-managed configuration before operational use. <br>
Risk: Optional AlphaVantage, Tavily, or Tushare credentials may be present in the runtime environment. <br>
Mitigation: Audit those environment variables and scope keys to the minimum services needed for the briefing workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinfi-codex/iran-war-tracker-v2) <br>
- [Ceasefire-period framework](artifact/【FRAME】停火期.md) <br>
- [Daily report template](artifact/【TEMPLATE】.md) <br>
- [Iran situation variables and economic impact framework](artifact/伊朗局势关键变量与经济影响分析框架.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown report with optional JSON or normalized feed data from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefings are expected to distinguish confirmed facts, market pricing signals, and scenario judgments, with reports capped by the skill guidance at about 3000 Chinese characters.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
