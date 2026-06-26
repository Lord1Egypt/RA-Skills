## Description: <br>
Use when creating a new internal application from scratch, standardizing a 0-to-1 app build workflow, or helping teammates bootstrap a Next.js/FastAPI/Keycloak/PostgreSQL style product with a docs-first process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyc-chengzi](https://clawhub.ai/user/lyc-chengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and internal app teams use this skill to clarify requirements, propose architecture, document decisions, bootstrap full-stack application structure, and validate delivery readiness before handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce architecture and implementation guidance that may be applied before business requirements and constraints are confirmed. <br>
Mitigation: Confirm requirements, MVP scope, architecture, authentication, database, storage, and access-control constraints before implementation. <br>
Risk: Generated repository changes could affect auth, database migrations, storage, or production configuration in shared environments. <br>
Mitigation: Review generated changes, avoid placing secrets in files or chat, and validate auth, migration, storage, and runtime configuration before applying them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lyc-chengzi/new-app) <br>
- [Requirements template](templates/requirements-template.md) <br>
- [Delivery checklist](templates/delivery-checklist.md) <br>
- [Chinese requirements template](templates/requirements-template.cn.md) <br>
- [Chinese delivery checklist](templates/delivery-checklist.cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with implementation notes, checklists, code/configuration changes, and validation commands when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce bilingual documentation updates and delivery checklists when the target application workflow requires them.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
