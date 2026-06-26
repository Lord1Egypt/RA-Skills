## Description: <br>
Hermes Learning syncs self-updated learning materials from Hermes Agent into WorkBuddy, including persistent evolution.db memory entries, concept links, and a feedback loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to transfer Hermes learning summaries into WorkBuddy so WorkBuddy can maintain strategy patterns, optimization notes, concept links, and feedback reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change WorkBuddy memory by importing Hermes learning summaries and writing to evolution.db. <br>
Mitigation: Review ~/.hermes/shared/memory_summary.json and workbuddy_feedback.json before applying, back up ~/.workbuddy/memory/evolution.db when it matters, and avoid automatic scheduled use unless ongoing memory updates are intended. <br>


## Reference(s): <br>
- [Hermes Learning on ClawHub](https://clawhub.ai/liuboacean/hermes-learning) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text output, JSON state files, and SQLite memory updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Hermes shared JSON files and can persist WorkBuddy memory updates in evolution.db.] <br>

## Skill Version(s): <br>
4.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
