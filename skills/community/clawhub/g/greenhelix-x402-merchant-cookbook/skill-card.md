## Description: <br>
Practical recipes for integrating x402 payments into web services, including Express.js middleware, FastAPI integration, Cloudflare Workers, payment verification, settlement, and production deployment patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add x402 crypto payment gates to APIs and web services. It provides implementation guidance and examples for Node.js, Python, and Cloudflare Workers deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes payment automation patterns that may spend funds or sign payment payloads without sufficient user-control safeguards. <br>
Mitigation: Require explicit approval, budget limits, merchant allowlists, and transaction logging before enabling automated payment flows. <br>
Risk: The skill references sensitive payment credentials including signing keys and Stripe API keys. <br>
Mitigation: Use sandbox credentials first and avoid providing live Stripe keys or signing keys unless a reviewed snippet specifically requires them. <br>
Risk: Example implementations may be copied into production before security, settlement, and accounting controls are reviewed. <br>
Mitigation: Review and test copied examples in a sandbox environment before deployment, then add logging and operational controls for settlement behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-x402-merchant-cookbook) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [x402 facilitator endpoint](https://x402.org/facilitator) <br>
- [x402 protocol specification](https://www.x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guide with code blocks, shell commands, configuration examples, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes illustrative payment-flow examples and environment-variable guidance; the artifact is not executable.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
