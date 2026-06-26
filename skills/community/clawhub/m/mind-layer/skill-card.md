## Description: <br>
我的脑子 provides a six-layer AI memory framework for OpenClaw agents, with rules and templates for long-term memory, user preferences, daily reflection, and archival review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z44264677](https://clawhub.ai/user/z44264677) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers can use this skill to structure persistent local memory, prioritize what should be remembered, and maintain profile, experience, and daily reflection files. It is intended for assistants that need personalized recall and memory hygiene across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to create and maintain persistent local memory, including user profiles, preferences, decisions, and experience records. <br>
Mitigation: Review USER.md, MEMORY.md, and memory/ regularly; avoid saving secrets or highly sensitive personal data; delete or redact entries that should no longer be retained. <br>
Risk: The artifact includes memory and communication rules that may influence how an agent stores and recalls user information. <br>
Mitigation: Review the rules and templates before installation, and adapt them to the user's privacy, retention, and compliance expectations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/z44264677/mind-layer) <br>
- [README.md](README.md) <br>
- [Rules](rules/RULES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown rules, templates, and installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persistent local memory files should be reviewed as sensitive user data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
