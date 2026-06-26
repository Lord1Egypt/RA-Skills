## Description: <br>
Synthesizes member-parent markdown reports into a continuous narrative. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeanLeeFumu](https://clawhub.ai/user/DeanLeeFumu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to turn multiple member markdown reports into one cohesive daily progress summary grouped by team member. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads all markdown files under ~/openclaw_agent/src/temp_sync/ and may include unintended local report content in the daily summary. <br>
Mitigation: Before running it, confirm that the source folder contains only markdown reports intended for summarization. <br>
Risk: A generated dated summary may overwrite an existing file at the target path. <br>
Mitigation: Check for an existing summary for the same UTC+8 date before execution when preserving prior output matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DeanLeeFumu/group-summarizer) <br>
- [Publisher profile](https://clawhub.ai/user/DeanLeeFumu) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files] <br>
**Output Format:** [Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a UTC+8 date-stamped daily summary under ~/openclaw_agent/src/latest_summaries/daily/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
