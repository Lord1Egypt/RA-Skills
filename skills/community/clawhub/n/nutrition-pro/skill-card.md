## Description:

Personal Nutritionist helps an agent log meals, estimate nutrition and calorie burn, track daily goals, maintain nutrition memory, and set optional reminders through conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javi23ruiz](https://clawhub.ai/user/javi23ruiz)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for conversational nutrition tracking, including meal logging, calorie and macro estimates, daily summaries, trend review, and optional proactive reminders. Agents use it to maintain a persistent nutrition profile and memory-backed history for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can build a lasting health-adjacent profile with nutrition goals, allergies, meal timing, preferences, patterns, and health context.

Mitigation: Install only when persistent nutrition memory is acceptable, review MEMORY.md contents periodically, and remove health context that should not be retained.

Risk: The skill can update memory silently after onboarding, including weekly rewrites of the user's profile and pattern summary.

Mitigation: Review memory updates during early use and keep only explicitly stated health details; do not rely on inferred diagnoses or medical conclusions.

Risk: The skill can add heartbeat behavior and optional OpenClaw cron reminders that continue to prompt or run later.

Mitigation: Confirm reminder choices before enabling them, then inspect HEARTBEAT.md and openclaw cron entries and disable any reminder that is not wanted.

Risk: Nutrition, calorie burn, and TDEE outputs are estimates and may be wrong for medical or clinical decisions.

Mitigation: Treat outputs as general tracking guidance, require user confirmation before logging uncertain portions, and consult qualified professionals for medical nutrition needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/javi23ruiz/skills/nutrition-pro)
- [Publisher profile](https://clawhub.ai/user/javi23ruiz)
- [ONBOARDING.md](artifact/ONBOARDING.md)
- [MEMORY_TEMPLATE.md](artifact/MEMORY_TEMPLATE.md)
- [HEARTBEAT_SNIPPET.md](artifact/HEARTBEAT_SNIPPET.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation responses, memory file entries, and optional OpenClaw cron commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update persistent memory files and create optional reminders after user confirmation.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
