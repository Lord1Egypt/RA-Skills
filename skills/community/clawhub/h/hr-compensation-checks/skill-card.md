## Description: <br>
Help HR teams with compensation review, band and market checks, and payroll filing prechecks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashley-aihr](https://clawhub.ai/user/ashley-aihr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR compensation and payroll teams use this skill to review compensation bands, market inputs, internal equity, offer positioning, and China payroll filing readiness before taking action. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Generated DOCX, CSV, and JSON outputs may persist sensitive HR, payroll, compensation, identity, or bank-related data in plaintext. <br>
Mitigation: Use masked identifiers and status-only fields where possible, write outputs only to protected locations, and apply an approved retention or deletion policy. <br>
Risk: Compensation and payroll guidance may be used without the required human or compliance review. <br>
Mitigation: Require authorized HR, payroll, finance, or compliance confirmation before using outputs for filing, offer, or compensation decisions. <br>


## Reference(s): <br>
- [Compensation Decision Assistant](SKILL.md) <br>
- [Real User Scenario](references/real-user-scenario.md) <br>
- [China HR Compensation Workflows](references/compensation-workflows.md) <br>
- [China Compensation Policy Knowledge Base 2026](references/china-compensation-policy-kb-2026.md) <br>
- [Dynamic Market Data Architecture](references/dynamic-market-data-architecture.md) <br>
- [Project homepage from ClawHub metadata](https://github.com/Ashley-AIHR/hrskill-compensation-module) <br>
- [ClawHub skill page](https://clawhub.ai/ashley-aihr/hr-compensation-checks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Structured Markdown guidance with optional generated DOCX, CSV, and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use COMP_EXPORT_PATH as an optional local export path for filing check outputs.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
