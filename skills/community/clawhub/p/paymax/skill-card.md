## Description: <br>
Paymax recognizes payment intents or payment parameters from other skills, creates payment requests through an external payment API, and returns the trade code and payment link for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sayxxx](https://clawhub.ai/user/sayxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and calling skills use Paymax to collect a payment amount, create a payment request, and present the resulting trade code and payment link. Operators should verify the payee, amount, and destination link before any real payment is completed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment details may be sent to an unverified external payment service. <br>
Mitigation: Use only when the operator of pay.4199191.xyz is trusted, and test first with non-sensitive payment data. <br>
Risk: A payment request may be created without a clear final user confirmation or provider disclosure. <br>
Mitigation: Require manual verification of the amount, payee, and payment link before completing any real payment. <br>
Risk: Other skills may invoke this skill with payment parameters. <br>
Mitigation: Treat calls from other skills as payment requests that still need user-visible review before payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sayxxx/paymax) <br>
- [Publisher profile](https://clawhub.ai/user/sayxxx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with payment status text, tradeCode, tradeLink, and optional shell command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Payment request output may include a tradeCode and tradeLink returned by the external payment service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
