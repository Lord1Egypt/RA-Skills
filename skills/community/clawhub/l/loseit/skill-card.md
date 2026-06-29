## Description: <br>
Lose It Nutrition lets an agent read a user's Lose It! data export and emit per-day nutrition JSON without modifying the account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stozo04](https://clawhub.ai/user/stozo04) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to authenticate to their own Lose It account or parse a downloaded export ZIP, then provide per-day nutrition JSON to an agent or downstream workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Lose It email/password credentials and a reusable local liauth session token. <br>
Mitigation: Prefer environment variables or a private config location, keep config and token files owner-only, and avoid shared folders, logs, screenshots, and backups. <br>
Risk: Downloaded export ZIPs and emitted nutrition JSON can contain personal nutrition data. <br>
Mitigation: Store exports and generated output only in private locations and remove them when they are no longer needed. <br>
Risk: Custom login or export URLs could send credentials or nutrition exports to unintended endpoints. <br>
Mitigation: Use the default Lose It HTTPS endpoints unless a custom LOSEIT_LOGIN_URL or LOSEIT_EXPORT_URL has been reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stozo04/loseit) <br>
- [Lose It CLI Repository](https://github.com/stozo04/loseit-cli) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON nutrition data with Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Nutrition output is keyed by ISO date and may include calories, macronutrients, fiber, meals, budget, under-budget, and exercise-adjustment fields.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
