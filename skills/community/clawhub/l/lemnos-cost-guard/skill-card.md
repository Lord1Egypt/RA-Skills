## Description: <br>
Lemnos Cost Guard helps OpenClaw agents track API costs, detect context bloat, enforce budget alerts, and recommend lower-cost model routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[getlemnos32](https://clawhub.ai/user/getlemnos32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw API spend, log task-level token usage, generate daily or longer cost reports, and identify oversized context loads that may increase cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local session logs or workspace files and write cost-tracking JSONL logs. <br>
Mitigation: Run it only on intended projects, review the configured log paths, and avoid sensitive workspaces unless the logging scope has been confirmed. <br>


## Reference(s): <br>
- [Model Pricing & Routing Reference](references/model_pricing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/getlemnos32/lemnos-cost-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with JSONL cost log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost estimates depend on configured model pricing and available session or task logs.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
