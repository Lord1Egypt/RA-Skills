## Description: <br>
Generates personalized interaction guides by analyzing user conversations so assistants can adapt responses to user preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neuhanli](https://clawhub.ai/user/neuhanli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to build and maintain a local personalization profile from consented conversation signals, enabling customized responses while providing view, pause, reset, and delete controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores a local personalization profile and related logs that may contain personal preference data. <br>
Mitigation: Install only when persistent local personalization is desired, keep ISKILL_DATA_PATH unset or pointed at a private dedicated directory, and protect that directory with appropriate permissions. <br>
Risk: A generated profile can become inaccurate or include details the user later considers too sensitive. <br>
Mitigation: Use the skill's view, pause, reset, or delete commands to inspect, stop, clear, or remove personalization data. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/neuhanli/i-skill) <br>
- [Publisher profile](https://clawhub.ai/user/neuhanli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown profile, JSON state files, audit logs, and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persistent local personalization data is stored only after user activation and consent.] <br>

## Skill Version(s): <br>
3.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
