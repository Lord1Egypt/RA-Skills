## Description: <br>
OpenClaw Cost Guard audits OpenClaw configuration for budget gaps, costly model defaults, large token ceilings, recurring automation, and other denial-of-wallet risk signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[X-RayLuan](https://clawhub.ai/user/X-RayLuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review OpenClaw agent configurations before scaling usage. It helps identify missing budgets, expensive defaults, large token limits, recurring automation, and browser workflow patterns that can increase spend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The static audit may not match actual provider billing or live usage patterns. <br>
Mitigation: Confirm the config path before running the audit, then compare the JSON output with real provider invoices and usage telemetry. <br>


## Reference(s): <br>
- [Cost Guard Playbook](references/cost-playbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/X-RayLuan/openclaw-agent-cost-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON audit output from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script reports score, verdict, summary, findings, recommendations, guardrails, and evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
