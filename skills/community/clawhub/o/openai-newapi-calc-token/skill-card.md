## Description: <br>
Helps agents calculate, audit, implement, and review token pricing and billing formulas for OpenAI-style APIs, NewAPI-compatible gateways, cached input, quota consumption, recharge ratios, and cost comparison dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y-victor](https://clawhub.ai/user/y-victor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to calculate and audit token billing formulas, avoid double-counting cached input tokens, normalize per-1K and per-1M prices, and separate quota calculations from money conversions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token-cost calculations can be wrong if token counts, current provider pricing, cache semantics, or recharge ratios are supplied incorrectly. <br>
Mitigation: Verify the billing mode, normalize price units, clamp cached tokens to total input, and review expanded formulas against current provider or gateway pricing before relying on results. <br>


## Reference(s): <br>
- [Token Cost Formula Reference](references/formulas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with formulas, worked examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows expanded formulas and final results for auditability; no external tools, credentials, or network access are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
