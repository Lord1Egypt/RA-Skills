## Description: <br>
Query Pinax API datasets, including Token API for EVM/SVM/TVM token data, prediction markets, and perp exchange data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinax](https://clawhub.ai/user/pinax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose Pinax API endpoints, construct authenticated requests, handle pagination and filters, and discover supported networks for token, prediction-market, and perp-exchange datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens and API keys could be exposed if copied into logs, shared transcripts, or unintended endpoints. <br>
Mitigation: Send credentials only to the intended Pinax API over HTTPS, avoid logging or sharing them, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [Pinax API base URL](https://api.pinax.network) <br>
- [Pinax API documentation](https://app.pinax.network/docs) <br>
- [Pinax FAQ](https://app.pinax.network/help) <br>
- [The Graph Market](https://thegraph.market) <br>
- [Pinax API Skill Card](https://clawhub.ai/pinax/pinax-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, code, configuration] <br>
**Output Format:** [Markdown with API endpoint paths, request headers, query parameters, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include endpoint selection guidance, pagination patterns, authentication headers, and request construction examples.] <br>

## Skill Version(s): <br>
3.21.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
