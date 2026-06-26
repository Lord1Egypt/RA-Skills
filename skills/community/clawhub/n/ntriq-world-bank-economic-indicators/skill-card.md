## Description: <br>
Free API for World Bank economic indicators and macro data. No subscription. Access GDP, inflation, poverty rates, trade data, development metrics. Government data, pay-per-use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, analysts, and developers use this skill to retrieve World Bank economic indicators for investment research, country risk models, and academic data collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes the API as free while directing agents to a USDC pay-per-use endpoint. <br>
Mitigation: Require explicit confirmation before paid calls, set a clear spending cap, and communicate the $0.01 USDC per-call cost before use. <br>
Risk: The API uses crypto payments on Base mainnet. <br>
Mitigation: Verify the wallet, network, endpoint, and payment amount before authorizing any call. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-world-bank-economic-indicators) <br>
- [Ntriq x402 homepage](https://x402.ntriq.co.kr) <br>
- [Ntriq service catalog](https://x402.ntriq.co.kr/services) <br>
- [World Bank economic indicators endpoint](https://x402.ntriq.co.kr/world-bank-econ) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include country metadata, World Bank indicator labels, values, and years.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
