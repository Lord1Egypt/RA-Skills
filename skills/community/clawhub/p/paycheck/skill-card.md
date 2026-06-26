## Description: <br>
Calculate salary breakdowns with taxes and deductions. Use when estimating take-home pay, checking withholdings, comparing deductions, analyzing components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents can use this skill to record, review, search, and export paycheck-related notes and comparisons. It should be treated as a local record-keeping tool rather than a paycheck or tax calculator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advertised as a paycheck calculator but primarily records paycheck-related notes, which may mislead users expecting tax or withholding calculations. <br>
Mitigation: Use it only for local note logging, review any calculations independently, and do not rely on its output as tax, payroll, or financial advice. <br>
Risk: Pay details entered into the skill are saved locally under ~/.local/share/paycheck and can later be searched or exported from that machine. <br>
Mitigation: Avoid entering salary, tax ID, withholding, benefits, or payroll details unless local storage and later searchability are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/paycheck) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text on stdout plus local log and export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores timestamped entries under ~/.local/share/paycheck; no network access is required.] <br>

## Skill Version(s): <br>
2.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
