## Description: <br>
A budget-tracking library for AI agents that records expenses, income, budgets, savings goals, recurring transactions, reports, and SkillBoss-powered insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to manage budget records programmatically, including expenses, income, budgets, savings goals, recurring transactions, analytics, exports, backups, and optional SkillBoss-powered natural-language parsing or insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial data may be stored in the local data directory and included in exports or backups. <br>
Mitigation: Store the data directory, exports, and backups in protected locations and use CLAWHUB_DATA_PATH when a controlled storage path is required. <br>
Risk: Natural-language parsing and AI insights may send financial data to the SkillBoss API. <br>
Mitigation: Enable those features only for data you are comfortable sending to SkillBoss. <br>
Risk: The skill requires a sensitive SkillBoss API key for AI-powered features. <br>
Mitigation: Use a dedicated or revocable SkillBoss API key and keep it in environment configuration rather than committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/intelligent-budget-tracker-2) <br>
- [SkillBoss skill page](https://skillboss.co/skills/intelligent-budget-tracker) <br>
- [SkillBoss API Hub /v1/pilot](https://api.skillboss.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, files] <br>
**Output Format:** [Markdown documentation with TypeScript examples, JSON-like return shapes, and local export or backup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for natural-language parsing and AI insights; stores financial data locally and supports exports and backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
