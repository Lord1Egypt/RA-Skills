## Description: <br>
Register domain names via crypto payments (USDC, USDT, ETH, BTC), check availability, get pricing across 1000+ TLDs, and complete registration with on-chain stablecoin payments on Ethereum, Arbitrum, Base, or Optimism. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esokullu](https://clawhub.ai/user/esokullu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check domain availability, review pricing, guide crypto payment selection, register domains through LobsterDomains, and retrieve domain order details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill can involve real cryptocurrency payments for domain registration. <br>
Mitigation: Verify the LobsterDomains service, quoted price, payment chain, currency, receiving address, and transaction hash independently before registration. <br>
Risk: Registrant contact details, transaction hashes, API keys, and returned OpenSRS credentials are sensitive. <br>
Mitigation: Treat these values as sensitive, avoid retaining them in logs or files, and store returned domain management credentials in a password manager. <br>


## Reference(s): <br>
- [LobsterDomains homepage](https://lobsterdomains.xyz) <br>
- [LobsterDomains API keys](https://lobsterdomains.xyz/api-keys) <br>
- [LobsterDomains pricing](https://lobsterdomains.xyz/pricing) <br>
- [ClawHub skill page](https://clawhub.ai/esokullu/lobsterdomains) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with HTTP examples, JSON request and response examples, and shell environment setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include domain availability, pricing, payment-chain guidance, order status, and sensitive OpenSRS management credentials returned by the service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
