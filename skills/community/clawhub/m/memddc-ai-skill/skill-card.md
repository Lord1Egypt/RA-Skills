## Description: <br>
MemDDC helps agents maintain project documentation and code iteration context by scanning repositories, generating docs, building DDD models, compressing project memory, and synchronizing changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qihao123](https://clawhub.ai/user/qihao123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use MemDDC to create and refresh project knowledge, DDD constraints, relation maps, VCS summaries, and implementation guidance for ongoing maintenance or refactoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and store sensitive project knowledge, including code, configs, commit history, IDE metadata, and user documents. <br>
Mitigation: Install it only in repositories where that access is acceptable, and review .memddc contents before committing or sharing them. <br>
Risk: Database or integration discovery could expose live credentials or sensitive operational details. <br>
Mitigation: Provide redacted schema, DDL exports, or sanitized samples instead of live database credentials. <br>
Risk: Scans, AI submissions, and file updates can change or disclose project context without clear consent boundaries. <br>
Mitigation: Require explicit approval before scans, AI submission, or file updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qihao123/memddc-ai-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON configuration examples, and proposed code or shell-command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .memddc project memory, documentation, VCS analysis, and DDD model files when permitted.] <br>

## Skill Version(s): <br>
1.0.2 (source: release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
