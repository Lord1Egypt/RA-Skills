## Description: <br>
Nutrition CLI helps agents look up nutrition data, log meals, track calories and macros against user goals, compare foods, estimate calorie burn, and summarize trends from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javi23ruiz](https://clawhub.ai/user/javi23ruiz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to set up nutrition tracking, answer food and calorie questions, log confirmed meals, and review daily or weekly intake trends using the nutrition CLI and private memory notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent storage may include sensitive meals, calorie goals, allergies, preferences, meal times, and health-related notes. <br>
Mitigation: Use the skill in private contexts, review MEMORY.md and daily memory notes after setup, and remove details that should not be retained. <br>
Risk: Proactive reminders and heartbeat behavior can prompt the user or run nutrition logging flows over time. <br>
Mitigation: Create reminders only after explicit user choice, review HEARTBEAT.md and cron entries, and disable any nutrition cron jobs that are no longer wanted. <br>
Risk: The skill depends on the external nutrition-cli pip package and nutrition data returned by its sources. <br>
Mitigation: Verify the installed package before relying on it and preserve source transparency when presenting USDA or Open Food Facts results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/javi23ruiz/nutrition-cli) <br>
- [Publisher profile](https://clawhub.ai/user/javi23ruiz) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Onboarding guide](artifact/ONBOARDING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and structured nutrition summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md, daily memory notes, HEARTBEAT.md, nutrition-cli configuration, and user-approved cron reminders.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
