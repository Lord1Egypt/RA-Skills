## Description: <br>
Monitors work intensity during work-related conversations, tracks recent activity timestamps, and inserts break reminders based on continuous work duration and time-of-day signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkxsparke](https://clawhub.ai/user/zkxsparke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, analysts, designers, researchers, and other knowledge workers can use this skill to add lightweight break, meal, and overtime reminders during long assistant sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local hook records recent message-timing activity in ~/.claude/mindbreak_* state files. <br>
Mitigation: Install only with user consent, disclose the activity logging behavior, and provide a clear way to disable the hook and delete its state files. <br>
Risk: The skill can modify assistant replies by forcing break reminders while hiding the hook mechanism from the user. <br>
Mitigation: Prefer a transparent version that labels reminders, allows opt-out, and removes instructions that prevent the assistant from explaining why a reminder appeared. <br>


## Reference(s): <br>
- [MindBreak ClawHub Skill Page](https://clawhub.ai/zkxsparke/mindbreak) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown text with hook-triggered reminder prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append light break, meal, or overtime reminders as the final paragraph of an assistant response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
