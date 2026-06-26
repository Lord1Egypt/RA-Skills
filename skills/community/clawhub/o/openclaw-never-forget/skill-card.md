## Description: <br>
Openclaw Never Forget guides Openclaw to maintain bilingual persistent memory through daily episodic logs, periodic context snapshots, long-term knowledge extraction, and explicit recall workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyh1226](https://clawhub.ai/user/chenyh1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Openclaw users use this skill to preserve project context, user preferences, decisions, task history, and recallable summaries across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill continuously saves user and project context into persistent local memory files. <br>
Mitigation: Use it only when long-term local memory is desired, and regularly inspect, redact, or delete saved markdown files. <br>
Risk: Saved memory files may contain sensitive project context or personal preferences. <br>
Mitigation: Keep the memory folder out of public repositories and avoid sharing secrets while the skill is active. <br>
Risk: Recall output can be misleading if the requested history is not present in memory files. <br>
Mitigation: Follow the skill directive to state clearly when no record exists instead of fabricating history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenyh1226/openclaw-never-forget) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown memory logs and synthesized natural-language summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to append local memory files and summarize retrieved memory rather than paste raw logs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
