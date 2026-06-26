## Description: <br>
Fitness accountability for the Lofy AI assistant, including workout logging from natural language, meal tracking with calorie and protein estimates, PR detection, gym reminders, and progress reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrey401](https://clawhub.ai/user/harrey401) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to keep a local fitness log through natural conversation, including workouts, meals, personal records, weekly targets, and progress summaries. It is intended for accountability and tracking, not medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may retain sensitive fitness, meal, weight, goal, consistency, and injury or pain notes in a local JSON file. <br>
Mitigation: Use it only when local retention is acceptable, ask the agent to log only explicit requests, and periodically review or delete data/fitness.json. <br>
Risk: Fitness nudges or progress comments could be inappropriate when the user mentions injury or pain. <br>
Mitigation: Follow the artifact guidance to suggest rest for injury or pain and avoid encouraging the user to push through pain. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/harrey401/lofy-fitness) <br>
- [Publisher profile](https://clawhub.ai/user/harrey401) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Short natural-language responses, markdown summaries, and structured JSON fitness records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local fitness records when the user asks to log workouts, meals, goals, weight, or progress.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
