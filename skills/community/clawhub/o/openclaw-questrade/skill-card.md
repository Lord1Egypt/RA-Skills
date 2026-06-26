## Description: <br>
Execute and monitor stock trades for openclaw.ai workflows using Questrade's browser platform with Yahoo Finance cross-checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[witty-quotes25](https://clawhub.ai/user/witty-quotes25) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to prepare Questrade Web order tickets, compare broker data with Yahoo Finance snapshots, generate pre-trade or post-trade checklists, and reconcile manual fills while keeping credentials and sensitive account data user-side. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trade preparation artifacts could be mistaken for autonomous order execution or financial advice. <br>
Mitigation: Keep broker submission manual, verify symbol, side, quantity, order type, prices, and risk limits yourself, and rely on human confirmation as the source of execution truth. <br>
Risk: Broker exports, account identifiers, generated checklists, or execution logs may contain sensitive financial information. <br>
Mitigation: Keep generated files local or redacted, use masked identifiers by default, and never provide passwords, MFA codes, cookies, API keys, or session tokens to the agent. <br>
Risk: Market data can be stale or diverge between Questrade and Yahoo Finance. <br>
Mitigation: Refresh quotes before acting, enforce configured freshness and drift thresholds, and pause when broker and reference prices diverge beyond the user's tolerance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/witty-quotes25/openclaw-questrade) <br>
- [Open Claw Questrade Data Contracts](references/data-contracts.md) <br>
- [OpenClaw.ai Policy Compliance](references/openclaw-policy-compliance.md) <br>
- [Questrade Browser Playbook](references/questrade-browser-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, CSV, and concise execution-log text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local review and should keep broker credentials, MFA codes, cookies, API keys, session tokens, and unredacted account data out of prompts, files, and logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
