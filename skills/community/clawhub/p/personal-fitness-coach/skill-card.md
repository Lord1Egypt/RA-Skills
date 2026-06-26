## Description: <br>
Personal Fitness Coach provides fitness and nutrition coaching personas for meal planning, macro management, workout programming, and progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ekintkara](https://clawhub.ai/user/ekintkara) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to get structured fitness and nutrition guidance, including meal planning, macro calculations, workout programming, and local meal or workout logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect sensitive health, diet, injury, body-composition, meal, and workout details in local logs. <br>
Mitigation: Review before installing in shared environments; avoid entering details that should not be stored locally, and inspect or remove local fitness logs when they are no longer needed. <br>
Risk: The skill presents medical-adjacent coaching through real-sounding dietitian and trainer personas. <br>
Mitigation: Treat the coaches as AI personas rather than verified licensed professionals, and seek qualified medical or fitness advice for health conditions, injuries, or clinical nutrition decisions. <br>
Risk: The helper scripts accept dates and write files without documented path validation, deletion, or export guidance. <br>
Mitigation: Use normal YYYY-MM-DD dates and the scripts' intended meal or workout logging workflows until path validation and log management guidance are added. <br>


## Reference(s): <br>
- [Calorie Guide](references/calorie-guide.md) <br>
- [Exercise Database](references/exercise-database.md) <br>
- [ClawHub skill page](https://clawhub.ai/ekintkara/personal-fitness-coach) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON-backed local logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts write meal and workout logs under the user's local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
