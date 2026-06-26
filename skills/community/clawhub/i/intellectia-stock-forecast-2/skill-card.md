## Description: <br>
US Stock AI Trading Assistant via SkillBoss API Hub for stock entry and exit analysis, target price predictions, probability calculations, technical ratings, and "Should I Buy" investment Q&A. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request one-symbol stock or crypto forecasts and structured buy, sell, or hold style analysis through SkillBoss API Hub. Outputs are informational and should not be treated as financial, investment, or trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols and financial-analysis questions are sent to SkillBoss using the user's API key. <br>
Mitigation: Do not include account numbers, private portfolio details, proprietary trading strategies, or other confidential information in prompts. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Provide SKILLBOSS_API_KEY through the environment and avoid pasting the key into prompts, shared transcripts, or committed files. <br>
Risk: Forecasts and buy, sell, or hold analysis may be incomplete, stale, or unsuitable for investment decisions. <br>
Mitigation: Treat outputs as informational only and verify decisions with authoritative financial data sources or a qualified professional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/intellectia-stock-forecast-2) <br>
- [SkillBoss skill page](https://skillboss.co/skills/intellectia-stock-forecast) <br>
- [SkillBoss API Hub pilot endpoint](https://api.skillboss.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with cURL and Python examples; SkillBoss API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends ticker symbols plus financial-analysis prompts to SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
