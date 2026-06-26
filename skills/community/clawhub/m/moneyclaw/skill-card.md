## Description: <br>
MoneyClaw helps OpenClaw agents inspect prepaid wallet readiness, create bounded payment tasks, and continue explicitly requested payment steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elvismusli](https://clawhub.ai/user/elvismusli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect MoneyClaw account readiness, create auditable prepaid payment tasks, and continue user-confirmed checkout steps. Merchant-side acquiring guidance is available only when the user explicitly wants to accept payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real payment activity through MoneyClaw, including checkout continuation and payment credential retrieval. <br>
Mitigation: Use prepaid balances, verify the merchant domain and amount before spending, keep agent auto-approval disabled unless intentional, and continue payment steps only after explicit user confirmation. <br>
Risk: Merchant-side acquiring guidance can enable account setting changes, invoice creation, and webhook secret handling. <br>
Mitigation: Use acquiring endpoints only when the user deliberately wants to accept payments, store webhook secrets carefully, and confirm server-side payment status before fulfilling orders. <br>


## Reference(s): <br>
- [MoneyClaw OpenClaw homepage](https://moneyclaw.ai/openclaw) <br>
- [Payment Safety Reference](references/payment-safety.md) <br>
- [Acquiring Reference](references/acquiring.md) <br>
- [MoneyClaw Skill Page](https://clawhub.ai/elvismusli/moneyclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require MONEYCLAW_API_KEY and explicit user approval before payment execution steps.] <br>

## Skill Version(s): <br>
5.5.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
