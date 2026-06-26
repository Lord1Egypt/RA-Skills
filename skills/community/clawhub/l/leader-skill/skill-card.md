## Description: <br>
Creates leader-specific AI skills from authorized workplace inputs to simulate leadership decisions, guide upward communication, and support career-development planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and career-development users use this skill to create a reusable leader profile for leadership simulation, upward-management preparation, and legitimate career growth planning. It is intended for use only with workplace data the user is authorized to process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect and store sensitive workplace chats, documents, generated leader profiles, backups, tokens, and local configuration. <br>
Mitigation: Install and run it only with clear authorization, avoid private chats, coworker identifiers, and company documents unless all consent and workplace approvals are in place, and delete generated files, backups, tokens, and ~/.create-leader configuration when finished. <br>
Risk: Leader weakness analysis and replacement-path planning can create harmful, defamatory, or unfair workplace guidance if based on unverified or private material. <br>
Mitigation: Use outputs for personal learning and legitimate career development only, review generated profiles before use, remove unverified negative claims, and do not share analysis without appropriate permission. <br>
Risk: OAuth or app credentials used for Feishu or DingTalk collection may expose additional workplace data if over-scoped or retained. <br>
Mitigation: Use least-privilege credentials, do not use admin keys, store tokens locally only, and revoke or rotate credentials after collection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuqingsonga/leader-skill) <br>
- [Publisher profile](https://clawhub.ai/user/zhuqingsonga) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON metadata, Python helper outputs, and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese workflow; generated leader skills are written under leaders/{slug}/ with local knowledge, version, and metadata files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
