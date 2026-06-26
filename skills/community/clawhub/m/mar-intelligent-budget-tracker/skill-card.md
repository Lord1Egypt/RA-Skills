## Description: <br>
Intelligent budget tracking and financial management library for AI agents - expense tracking, income management, budgets, savings goals, and SkillBoss API Hub-powered insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to add programmatic expense tracking, income management, budgeting, savings goals, recurring transactions, analytics, reports, and AI-assisted financial insights to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle sensitive financial details and send spending data to SkillBoss for parsing and insights. <br>
Mitigation: Install only if you trust the npm package and SkillBoss; keep the API key in a protected environment variable and avoid sending unnecessary sensitive details. <br>
Risk: Budget data, backups, and exports may contain private financial records. <br>
Mitigation: Use a private storage path, protect backup and export files, and control access to the configured data directory. <br>
Risk: Automated agents could add transactions or process recurring entries without sufficient user confirmation. <br>
Mitigation: Have the agent ask before adding transactions or processing recurring entries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/mar-intelligent-budget-tracker) <br>
- [SkillBoss Intelligent Budget Tracker](https://skillboss.co/skills/intelligent-budget-tracker) <br>
- [SkillBoss API Hub Pilot Endpoint](https://api.skillboss.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, environment configuration, and structured financial data outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for natural language parsing and AI-powered insights; may read and write local budget data and backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
