## Description: <br>
Provides pay-per-use access to UN Sustainable Development Goals tracking data from World Bank sources by country, region, or globally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents can query SDG indicators for impact investment reporting, development program monitoring, and ESG sustainability analysis across countries, regions, or the world. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes a free data source while its access instructions use a paid x402 endpoint at $0.01 USDC per call. <br>
Mitigation: Configure the agent to ask before each paid request and enforce a strict spending limit before enabling purchase capability. <br>
Risk: The skill uses crypto micropayments on Base for API access. <br>
Mitigation: Enable it only in environments approved for x402/USDC payments and review wallet, network, and authorization settings before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-world-bank-development-goals) <br>
- [Publisher profile](https://clawhub.ai/user/ntriq-gh) <br>
- [ntriq x402 homepage](https://x402.ntriq.co.kr) <br>
- [World Bank Goals endpoint](https://x402.ntriq.co.kr/world-bank-goals) <br>
- [Service catalog](https://x402.ntriq.co.kr/services) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown with endpoint examples and JSON response shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate paid x402/USDC requests when used by an agent configured to make purchases.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
