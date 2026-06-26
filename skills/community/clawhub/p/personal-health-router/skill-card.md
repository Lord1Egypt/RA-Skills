## Description: <br>
Tracks meals, sleep quality, workouts, and recovery signals with automated Feishu/Lark persistence, summaries, and dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neverwarm](https://clawhub.ai/user/neverwarm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to log and analyze meals, sleep, recovery, and workout data, then persist records and refresh health summaries in Feishu/Lark. Developers and operators can also use it to bootstrap the configured health tables and run weekly or monthly reporting scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store sensitive meal, sleep, recovery, and workout records in Feishu/Lark. <br>
Mitigation: Use a dedicated Feishu/Lark base with limited sharing, keep the base token narrowly scoped, and avoid adding unrelated personal data. <br>
Risk: Upsert, rebuild, backfill, bootstrap, and dashboard refresh actions can write or rewrite health records. <br>
Mitigation: Run available dry-run commands first and require the agent to show the exact target table and fields before allowing write operations. <br>
Risk: Consumer health and wearable data can be mistaken for clinical evidence. <br>
Mitigation: Keep outputs non-diagnostic, separate observed data from suggestions, and state uncertainty when values are estimated or missing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/neverwarm/personal-health-router) <br>
- [README](README.md) <br>
- [Config Template](references/config-template.md) <br>
- [Public Data Model](references/data-model.md) <br>
- [Nutrition Branch](references/nutrition.md) <br>
- [Sleep Branch](references/sleep.md) <br>
- [Exercise Branch](references/exercise.md) <br>
- [Cross-Domain Branch](references/cross-domain.md) <br>
- [Weekly Health Review](references/weekly-review.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured health observations, uncertainty notes, configuration guidance, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run Node.js, Python, and lark-cli commands against a user-configured Feishu/Lark base.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
