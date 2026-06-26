## Description: <br>
Use when an OpenClawBot needs to create or verify PayTrigo payments on Base/USDC without webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paytrigo](https://clawhub.ai/user/paytrigo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClawBot operators use this skill to create PayTrigo invoices, guide browser-based user payments, run direct bot payment flows, and poll payment status on Base/USDC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships live PayTrigo payment API credentials, which creates shared-credential and production-use risk. <br>
Mitigation: Prefer a version configured with your own scoped credential before production use. <br>
Risk: Direct bot payment flows can spend wallet funds if an agent is given a private key or passphrase file without external controls. <br>
Mitigation: Use external spend limits, approval checks, recipient verification, and avoid giving an agent private keys or passphrases unless necessary. <br>
Risk: Polling-only payment status can fail operationally if invoice state or checkout tokens are not retained. <br>
Mitigation: Persist invoiceId and checkoutToken for each payment attempt and continue polling until a documented terminal status is reached. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces polling-oriented payment flow instructions and local wallet setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
