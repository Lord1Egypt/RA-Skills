## Description: <br>
Fetch product info by payment link ID. Calls GStable API to get payment link details, returns product name, description, price, and supported payment tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TanksCar](https://clawhub.ai/user/TanksCar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect GStable payment links before payment by retrieving product details, prices, and supported payment tokens from a link ID or payment URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper sends inspected payment link IDs to GStable, or to an alternate service if GSTABLE_API_BASE_URL is changed. <br>
Mitigation: Use the default GStable API endpoint unless the alternate endpoint is trusted, and avoid submitting link IDs that should not be shared with that service. <br>
Risk: The skill requires installing npm dependencies before running the command-line helper. <br>
Mitigation: Review and install the locked dependencies in a controlled skill directory before using the helper. <br>


## Reference(s): <br>
- [GStable Get Payment Link API documentation](https://docs.gstable.io/zh-Hans/docs/api/ai-payment/get-payment-link/) <br>
- [Payment Link Reader on ClawHub](https://clawhub.ai/TanksCar/payment-link-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from the command-line helper, with agent-facing summaries in text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns link ID, link name, product details, prices, attributes, and supported payment token summaries when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
