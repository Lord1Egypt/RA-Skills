## Description: <br>
Track nutrition, meals, water, weight, steps, meditation, journal entries, and AI coaching through the Habit AI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[habitclaw](https://clawhub.ai/user/habitclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to log meals, water, weight, steps, meditation, and journal entries, then retrieve nutrition summaries and coaching from Habit AI. It is intended for personal health tracking workflows that require a Habit AI account and API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive health-related text, food photos, journal entries, weight, and similar data to Habit AI. <br>
Mitigation: Share only information needed for the task, avoid secrets or unnecessary medical details, and review Habit AI's privacy and deletion practices before use. <br>
Risk: Nutrition estimates generated from descriptions or photos may be uncertain. <br>
Mitigation: Treat nutrition analysis as an estimate and review values before logging or relying on them for health decisions. <br>


## Reference(s): <br>
- [Habit AI API Reference](references/api.md) <br>
- [Habit AI](https://habitapp.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/habitclaw/habit-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses HABITAI_API_KEY for authenticated Habit AI API requests.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
