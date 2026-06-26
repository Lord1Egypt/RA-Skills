## Description: <br>
Multi-Agent system for writing ultra-long feasibility study reports. Phase 0 Requirement Confirmation - Phase 1 Planner outputs outline - Phase 2 Batch parallel sub-Agent writing - Phase 2.5 Cross-chapter consistency review - Phase 3 Integrator assembles polished docx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinqiu193](https://clawhub.ai/user/jinqiu193) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to plan, draft, review, and assemble long feasibility-study reports with multiple agent writing phases, chapter tracking, consistency checks, and formatted DOCX output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, modify, and overwrite local report state and generated files. <br>
Mitigation: Run it in a dedicated work directory, configure output paths deliberately, and review generated files before replacing production documents. <br>
Risk: The skill can spawn multi-agent writing workflows and invoke external Mermaid tooling. <br>
Mitigation: Use trusted local environments, keep Mermaid and npx rendering disabled unless needed, and review tool execution before enabling optional rendering. <br>
Risk: Optional Feishu or OpenClaw Weixin notifications may send information outside the local machine. <br>
Mitigation: Keep notifications on the default log channel unless external sharing is intended and approved for the report material. <br>
Risk: Reference materials may contain confidential content that is retained in local working files. <br>
Mitigation: Avoid confidential source material unless local retention is acceptable and clear or isolate sensitive projects in controlled workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinqiu193/lobsterai-report-agent) <br>
- [Phase 0 requirement confirmation guide](references/phase0_guide.md) <br>
- [Phase 1 planner guide](references/phase1_guide.md) <br>
- [Phase 2 sub-agent writing guide](references/phase2_guide.md) <br>
- [Markdown table format guide](references/table_format_guide.md) <br>
- [Bug fix and rebuild guide](references/bug_fix_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated report artifacts are local DOCX, JSON, and text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may create or modify local chapter state, report outputs, glossary files, tracker files, and notification logs according to its configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
