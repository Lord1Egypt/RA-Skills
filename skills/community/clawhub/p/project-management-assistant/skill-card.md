## Description: <br>
项目管理助手（PM Assistant）协助项目经理和交付团队完成项目启动信息提取、WBS任务分解、项目进度整理、项目风险预警、周报生成、客户沟通跟踪、交付物验收归档与项目复盘。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afeicn](https://clawhub.ai/user/afeicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project managers, delivery managers, and business operations teams use this skill to turn project materials and team updates into structured plans, status summaries, risk registers, weekly reports, customer follow-up drafts, archive records, and retrospective notes. It is designed to support human review rather than make final scope, commitment, delay, customer response, or acceptance decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project materials may contain contracts, financial data, customer communications, employee information, or other sensitive business content. <br>
Mitigation: Configure redaction, permission checks, retention and deletion rules, and archive access controls before using the skill with real business documents. <br>
Risk: Generated plans, customer response drafts, delivery commitments, delay judgments, scope changes, or acceptance conclusions could be mistaken for final decisions. <br>
Mitigation: Route scope changes, delivery commitments, project delay judgments, formal customer replies, and acceptance conclusions to an authorized human reviewer before external use. <br>
Risk: Feishu bot access, knowledge bases, logs, and archive locations can expose project records if deployed without role-appropriate permissions. <br>
Mitigation: Install only in permissioned environments and audit accesses, skill calls, confirmations, and archive paths. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/afeicn/project-management-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/afeicn) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [workflows.md](artifact/workflows.md) <br>
- [system_prompt.md](artifact/system_prompt.md) <br>
- [project_management_skills.yaml](artifact/skills/project_management_skills.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Structured Markdown and template-backed text outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include project conclusions, key facts, risks or gaps, suggested actions, required human confirmations, and archive records.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
