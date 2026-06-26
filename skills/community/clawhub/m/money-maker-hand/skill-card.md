## Description: <br>
Autonomous money-making assistant that researches market opportunities, evaluates earning options, tracks income progress, and generates actionable reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bandwe](https://clawhub.ai/user/Bandwe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to research income opportunities across platforms, score options by market demand and monetization potential, and produce Markdown action plans with income tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store income goals, opportunity history, generated reports, and progress state. <br>
Mitigation: Review stored state such as income_database.json and money_maker_state, and clear it when the information should no longer be retained. <br>
Risk: Generated earning plans and opportunity scores may be inaccurate or unsuitable for a user's situation. <br>
Mitigation: Review market research, expected income, and action plans before spending money, publishing content, or accepting work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bandwe/money-maker-hand) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with optional JSON dashboard metrics and TOML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist income goals, opportunity history, reports, and progress state when the agent environment supports memory or file storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
