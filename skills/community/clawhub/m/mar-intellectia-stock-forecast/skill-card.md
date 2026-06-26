## Description: <br>
Provides stock and crypto forecasts, target-price predictions, probability estimates, technical ratings, and buy/sell/hold Q&A through SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request single-symbol stock or crypto forecasts and buy/sell/hold rationale through SkillBoss API Hub for informational analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols and investment questions are sent to SkillBoss API Hub. <br>
Mitigation: Keep SKILLBOSS_API_KEY in environment configuration and avoid submitting brokerage details, account data, or sensitive portfolio information. <br>
Risk: Forecasts and buy/sell/hold analysis may be inaccurate, delayed, or misleading. <br>
Mitigation: Treat results as informational only and verify important financial conclusions with licensed data sources or qualified professionals. <br>
Risk: API credentials can be exposed if copied into prompts, source files, or logs. <br>
Mitigation: Use environment variables for credentials and review commands before running or sharing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marjoriebroad/mar-intellectia-stock-forecast) <br>
- [SkillBoss Intellectia Stock Forecast](https://skillboss.co/skills/intellectia-stock-forecast) <br>
- [SkillBoss API Hub endpoint](https://api.skillboss.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with curl and Python examples, plus SkillBoss API results as text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends ticker symbols or investment questions to SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
