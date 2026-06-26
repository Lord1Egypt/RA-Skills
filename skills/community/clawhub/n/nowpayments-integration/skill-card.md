## Description: <br>
Integrates the NowPayments API so an agent can add multi-cryptocurrency checkout, IPN handling, and order tracking to an AI-operated store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and store operators use this skill to have an agent add NowPayments checkout, payment callbacks, status polling, and product configuration to an ecommerce store. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to modify payment code for a live store. <br>
Mitigation: Review generated checkout and callback code before deployment and test the flow in staging before accepting real payments. <br>
Risk: NowPayments API keys and IPN secrets could be exposed if placed in client-side code or committed to source control. <br>
Mitigation: Keep payment secrets server-side in environment variables and verify they are excluded from source control. <br>
Risk: Incorrect checkout or IPN handling could misreport payment status or order fulfillment. <br>
Mitigation: Verify IPN signature handling, rate limiting, CSRF protections, and order status transitions before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/casperzinou/nowpayments-integration) <br>
- [NowPayments API documentation](https://documenter.getpostman.com/view/7900902/S1a7UnNT) <br>
- [Store example](https://www.talonforge.xyz/store) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment variable setup, checkout endpoint guidance, IPN callback handling, status polling, and security checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
