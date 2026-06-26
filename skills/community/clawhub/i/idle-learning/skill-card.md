## Description: <br>
AI持续学习系统让 an agent periodically collect GitHub trends and arXiv papers, summarize findings, and save local learning notes for later memory distillation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freak30](https://clawhub.ai/user/freak30) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep a local AI assistant updated on public AI research and repository trends, especially topics around agent memory, reasoning, self-improvement, and related papers. It is intended for unattended periodic learning workflows that store concise local notes for later review or memory integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill periodically collects public GitHub and arXiv information and can introduce noisy, stale, or irrelevant findings into local learning notes. <br>
Mitigation: Review generated notes before using them as long-term memory, and tune the topics or schedules to match the deployed agent's purpose. <br>
Risk: Scheduled execution depends on local Python dependencies and an external mmx CLI for optional summarization. <br>
Mitigation: Confirm the Python packages and mmx CLI are installed from trusted sources before enabling automated runs. <br>
Risk: The skill writes learning records and logs to the local skill workspace. <br>
Mitigation: Verify the storage path and file permissions before scheduling the skill, and inspect generated files periodically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freak30/idle-learning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Local JSON learning records, Markdown study logs, terminal status text, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes recent learning items to learnings.json and appends summaries to study_log.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
