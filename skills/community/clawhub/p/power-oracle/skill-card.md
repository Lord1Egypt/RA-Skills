## Description: <br>
Use when the user wants Power Oracle to compute workout work or power from structured or shorthand workout details. Do not use for coaching or general fitness advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[workcapacity-io](https://clawhub.ai/user/workcapacity-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Power Oracle to validate workout movement inputs, build conservative split payloads, and request authoritative workout work and power results from the Power Oracle API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The compute endpoint may require x402 payment and can guide an agent through a paid API retry. <br>
Mitigation: Show the current price from /v1/payment-requirements and obtain explicit user approval before submitting any payment-capable retry. <br>
Risk: Workout and body details are sent to api.workcapacity.io for computation. <br>
Mitigation: Use the skill only when the user accepts sending those details to the third-party API. <br>
Risk: Unsupported or ambiguous movement names can produce invalid requests or misleading results. <br>
Mitigation: Call /v1/movements before compute when movement mapping or required inputs are uncertain, and ask the user for the minimum clarification needed. <br>


## Reference(s): <br>
- [API Contract](references/api-contract.md) <br>
- [Power Oracle Documentation](https://www.workcapacity.io/docs/power-oracle) <br>
- [Power Oracle ClawHub Listing](https://clawhub.ai/workcapacity-io/power-oracle) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with API request details, computed results, and explanatory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require x402 payment handling before returning authoritative compute results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
