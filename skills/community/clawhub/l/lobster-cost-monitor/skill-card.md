## Description: <br>
OpenClaw Cost Guardian monitors OpenClaw token use and estimated cost, recommends lower-cost models, issues budget alerts, and produces optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanqirong](https://clawhub.ai/user/zhanqirong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to review token spending, choose cost-appropriate models, receive budget warnings, and generate cost reports with optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks to inspect OpenClaw usage across conversations without clear opt-in, retention, deletion, or report-destination boundaries. <br>
Mitigation: Use it manually or only after explicit opt-in; limit analysis to the current reporting scope unless data handling and report destinations are documented. <br>
Risk: The skill describes automatic daily reports and possible cost-related behavior changes without confirmation controls. <br>
Mitigation: Require user confirmation before sending reports, changing models, pausing tasks, or applying budget-control actions. <br>
Risk: Model prices, budget status, and savings claims may be inaccurate if based on stale or incomplete usage data. <br>
Mitigation: Treat outputs as estimates and verify recommendations against current billing data before making spending or workflow decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zhanqirong/lobster-cost-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports with plain-text recommendations and YAML-style configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost estimates and savings recommendations depend on available usage and pricing data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
