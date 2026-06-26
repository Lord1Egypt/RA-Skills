## Description: <br>
HealthFit helps users manage fitness, nutrition, body metrics, TCM wellness, and optional sexual-health records through four role-specific advisors and local logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenChen913](https://clawhub.ai/user/ChenChen913) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use HealthFit as an agent-assisted wellness journal for workout planning, diet logging, health summaries, TCM constitution guidance, and local personal health record management. It is wellness support and should not be used as a substitute for medical diagnosis or care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores health, body, diet, medication/history, TCM, and optional sexual-health information in local plaintext files. <br>
Mitigation: Keep the data directory and generated export or backup folders out of shared and cloud-synced locations unless intentionally sharing them. <br>
Risk: Exports and backups can contain sensitive health information. <br>
Mitigation: Review exported files before sharing and leave optional private sexual-health records excluded unless explicit inclusion is intended. <br>
Risk: Health, fitness, nutrition, TCM, and sexual-health guidance may be mistaken for medical care. <br>
Mitigation: Treat responses as wellness support and seek qualified medical care for diagnosis, treatment, urgent symptoms, or condition-specific decisions. <br>


## Reference(s): <br>
- [HealthFit ClawHub Release](https://clawhub.ai/ChenChen913/healthfit) <br>
- [HealthFit Evidence Base](references/evidence_base.md) <br>
- [HealthFit Storage Schema](references/storage_schema.md) <br>
- [Quick Commands Instructions](references/commands.md) <br>
- [Western and TCM Onboarding Flow](references/onboarding.md) <br>
- [TCM Constitution Guide](references/tcm_constitution.md) <br>
- [Exercise Library](references/exercise_library.md) <br>
- [Nutrition Guidelines](references/nutrition_guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses, local file updates, and optional shell commands for backup, export, and database setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may reference or update local plaintext health logs and JSON profile files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter, config, and changelog state 3.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
