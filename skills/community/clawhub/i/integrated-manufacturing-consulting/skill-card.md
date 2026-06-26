## Description: <br>
Generates executive manufacturing consulting project summary reports from uploaded materials, combining department research methods, ODP-I² diagnostics, multi-format report generation, and industry report search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericshao2025](https://clawhub.ai/user/ericshao2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External consultants, internal operations leaders, and manufacturing engineers use this skill to turn uploaded project materials into executive-ready consulting summaries, diagnostics, improvement plans, and supporting report deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic upload processing can expose factory photos, production metrics, customer files, or generated reports. <br>
Mitigation: Use a controlled workspace and require explicit user approval before extracting, processing, or transferring confidential materials. <br>
Risk: The skill may scan local skills, write persistent logs, and modify its own SKILL.md instructions. <br>
Mitigation: Disable or require confirmation for local skill scanning, persistent logging, and self-repair writes; review diffs before reuse. <br>
Risk: Web searches and WeChat, QQ, or Tencent delivery can send information outside the local environment. <br>
Mitigation: Block external delivery and network search by default, enabling them only after the user approves the destination and content. <br>
Risk: Non-local Ollama endpoints may receive sensitive prompts or source content. <br>
Mitigation: Restrict model calls to localhost or trusted endpoints and verify endpoint configuration before processing private data. <br>


## Reference(s): <br>
- [Methodology](artifact/references/methodology.md) <br>
- [Diagnosis Framework](artifact/references/diagnosis_framework.md) <br>
- [Project Definition](artifact/references/project_definition.md) <br>
- [Report Templates](artifact/references/report-templates.md) <br>
- [Requirements Summary](artifact/references/requirements-summary.md) <br>
- [iResearch API Notes](artifact/references_industry_search/iresearch-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with generated consulting report content and optional PPTX, DOCX, PDF, and mindmap files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process uploaded documents and images, run local Python tooling, use web search, and call an optional Ollama endpoint depending on configuration.] <br>

## Skill Version(s): <br>
7.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
