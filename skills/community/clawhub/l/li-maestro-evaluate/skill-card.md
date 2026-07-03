## Description: <br>
Interactive CSA MAESTRO threat-modeling workflow for agentic AI systems and OpenCode Skills that produces risk assessment outputs with AI risk classification mapping to China's AI governance framework. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
Developers, security reviewers, and AI governance teams use this skill to run interactive threat modeling for agentic AI systems or OpenCode Skills. It supports quick MVTM checklist assessments and full 10-phase MAESTRO assessments with structured risk, mitigation, residual-risk, and AI risk-classification outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated threat-model reports may contain sensitive architecture, code, data-flow, or compliance details. <br>
Mitigation: Review generated files before sharing, store them in approved locations, and confirm the organization permits sending assessment content to the AI provider. <br>
Risk: Optional DOCX/XLSX generation depends on unpinned Python dependency ranges. <br>
Mitigation: Pin and review python-docx and openpyxl versions in controlled environments before enabling document-generation scripts. <br>
Risk: The artifact and server evidence disagree on the release license. <br>
Mitigation: Confirm authoritative license terms with the publisher before commercial use or redistribution. <br>


## Reference(s): <br>
- [MAESTRO Playbook](https://github.com/agentic-threat-modeling/MAESTRO) <br>
- [ClawHub Skill Page](https://clawhub.ai/43622283/skills/li-maestro-evaluate) <br>
- [Publisher Profile](https://clawhub.ai/user/43622283) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Interactive guidance plus Markdown, JSON, DOCX, and XLSX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-run local threat-model directories and optional Word/Excel reports.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata, SKILL.md frontmatter, manifest.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
