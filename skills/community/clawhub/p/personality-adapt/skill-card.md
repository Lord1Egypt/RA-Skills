## Description: <br>
Learns and adapts to the user's personality over time by observing communication style, values, decision-making patterns, and preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enjuguna](https://clawhub.ai/user/enjuguna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent maintain a visible personality profile and adapt its responses based on observed communication preferences, values, and decision patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill builds a persistent profile from private conversation notes and emotional signals. <br>
Mitigation: Review PERSONALITY.md and observations.json before use, and delete or edit sensitive or inaccurate observations. <br>
Risk: Scheduled observation and adaptation can continue collecting and updating personality data without active review. <br>
Mitigation: Use dry-run mode first and avoid enabling cron jobs until the stored data and behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/enjuguna/personality-adapt) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown profile notes, JSON observation logs, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run review before updating the personality profile.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
