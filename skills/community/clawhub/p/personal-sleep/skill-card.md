## Description: <br>
Acts as the user's sleep coach in the Sleep topic, tracking sleep schedule, quality, patterns, naps, and giving advice for better sleep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GekaCross](https://clawhub.ai/user/GekaCross) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals use this skill as a personal sleep coach to log bedtimes, wake times, sleep quality, naps, and notes. The agent analyzes the local sleep journal for patterns and provides supportive sleep hygiene guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may retain personal sleep details over time in a local sleep journal. <br>
Mitigation: Review, edit, or delete knowledge/personal/sleep.md when older sleep history should not be retained. <br>
Risk: Sleep notes could accidentally include sensitive secrets or agent instructions. <br>
Mitigation: Avoid putting secrets or agent instructions in the notes field. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GekaCross/personal-sleep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational text and Markdown sleep-log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update a local Markdown sleep journal at knowledge/personal/sleep.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
