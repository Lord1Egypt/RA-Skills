## Description: <br>
Plan and execute authorized Metasploit assessments for OpenClaw tasks with repeatable workflows covering target triage, module selection, option tuning, resource-script generation, controlled execution, and evidence-focused reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengyuxiu](https://clawhub.ai/user/zengyuxiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners and developers use this skill for authorized Metasploit assessments that require scoped target triage, module and payload selection, repeatable resource-script generation, controlled execution, and concise evidence-based reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Metasploit workflows can be misused or run outside an authorized assessment scope. <br>
Mitigation: Confirm written authorization, in-scope targets, test window, and prohibited techniques before any technical step. <br>
Risk: Generated resource scripts may execute unintended module, payload, listener, or target options if reviewed poorly. <br>
Mitigation: Review every generated .rc file before running msfconsole and confirm target, payload, listener, and optional settings. <br>
Risk: Logs, reports, or generated scripts may contain sensitive credentials or proof artifacts. <br>
Mitigation: Avoid storing real credentials in generated scripts and redact logs and reports before sharing. <br>


## Reference(s): <br>
- [Module Selection Heuristics](references/module-selection.md) <br>
- [Execution and Reporting Workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated Metasploit resource-script content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated .rc script text, scoped execution steps, check results, session evidence summaries, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
