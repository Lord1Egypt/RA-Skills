## Description: <br>
将聊天记录、截图文字、链接和随手记等碎片灵感整理为可检索知识库，支持快速收录、规则分类、关键词/近似语义检索和旧素材回顾。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nycxk](https://clawhub.ai/user/nycxk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, product builders, and note-heavy users use this skill to capture scattered inspiration into local JSON cards, classify it with editable topic rules, search past material, and review older entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks the release suspicious and describes broad local authority and possible fallback reviewer behavior involving external AI reviewer CLIs. <br>
Mitigation: Review the skill before installation, avoid running it on repositories containing secrets or private code, avoid full-access defaults, and configure fallback reviewer behavior explicitly. <br>
Risk: Captured inspiration text, URLs, and notes are persisted in a local JSON database, which may include personal or sensitive material if users collect it. <br>
Mitigation: Choose the database path deliberately, avoid storing secrets or private material, and review or delete entries before sharing the database. <br>


## Reference(s): <br>
- [Reference guide](reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/nycxk/inspiration-material-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [CLI text output plus local JSON knowledge-base entries and editable JSON topic rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data locally; database and rules paths can be overridden with INSPIRATION_DB_PATH and INSPIRATION_TOPIC_RULES_PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
