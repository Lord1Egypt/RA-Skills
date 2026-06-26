## Description: <br>
An AI weight-loss companion that calculates daily step goals from the previous day's calorie intake and uses step completion as the main coaching metric. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyoung310](https://clawhub.ai/user/joeyoung310) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for daily weight-loss coaching, meal and activity tracking, and step-goal supervision based on calorie estimates and local profile records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive health, meal, step, weight, and conversation-state data. <br>
Mitigation: Use it only where local health/activity tracking is acceptable, review stored records regularly, and delete profile or daily-record data when no longer needed. <br>
Risk: The skill provides supplement, fasting, binge-response, and menstrual-cycle coaching that may be mistaken for medical advice. <br>
Mitigation: Treat outputs as non-medical coaching, avoid using them for medical decisions, and consult a qualified professional for health conditions or restrictive diet plans. <br>
Risk: Device or app binding may expose step data outside the local skill context. <br>
Mitigation: Confirm what activity data will be shared before connecting a device or app, and verify how to disconnect or delete synced records. <br>


## Reference(s): <br>
- [Food Calories Reference](references/food_calories.md) <br>
- [ClawHub skill page](https://clawhub.ai/joeyoung310/kite-slim) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational guidance, Markdown reports, JSON-backed records, and optional HTML summary cards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local profile, daily record, and conversation-state JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
