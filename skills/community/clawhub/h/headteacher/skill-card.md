## Description: <br>
Bootstrap and operate an AI-native headteacher workspace for backend selection, Feishu Base access routing, schema installation, class data operations, and Office artifact generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzdame](https://clawhub.ai/user/yzdame) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External educators and agent users use this skill to initialize and operate a class-management workspace, record and query student data, inspect or migrate Feishu Bases, and generate working documents such as seat plans, duty schedules, and parent meeting slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive student records, contact details, local account metadata, and Feishu Base identifiers. <br>
Mitigation: Use only authorized class data, start with test or redacted data, restrict generated Office files, and avoid sharing logs or transcripts containing Base tokens or student information. <br>
Risk: Feishu workspace setup, bootstrap, import, export, or schema changes can affect cloud-hosted class data. <br>
Mitigation: Review Feishu permissions, inspect existing Bases before migration, run dry-runs where available, and preview destructive or schema-changing operations before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yzdame/headteacher) <br>
- [Product requirements summary](docs/PRD.md) <br>
- [Schema manifest](references/schema-manifest.md) <br>
- [Backend contract](references/backend-contract.md) <br>
- [Feishu model](references/feishu-model.md) <br>
- [Artifact specification](references/artifact-spec.md) <br>
- [Anthropic Office skills reference](https://github.com/anthropics/skills/tree/main/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration steps, and generated document or spreadsheet artifacts when dependencies are available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or register local Office files and workspace manifests after user confirmation.] <br>

## Skill Version(s): <br>
2.1.0 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
