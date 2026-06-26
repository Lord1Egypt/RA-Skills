## Description: <br>
Query Maestro APIs over HTTP using the SIWX + JWT + x402 credit purchase flow. Resolve the exact endpoint from docs.gomaestro.org before requesting or paying. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vardominator](https://clawhub.ai/user/Vardominator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to make direct HTTP calls to Maestro API endpoints, including SIWX authentication and x402 credit purchase handling when a live API response requires payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to sign wallet messages or use private-key access. <br>
Mitigation: Use a dedicated low-balance wallet or constrained runtime signer, and do not expose a high-value wallet private key. <br>
Risk: The skill can purchase Maestro API credits with USDC when a live 402 response requires payment. <br>
Mitigation: Require explicit approval for every paid request and verify the endpoint, network, payee, asset, and exact amount before signing. <br>
Risk: Payment parameters can change between attempts. <br>
Mitigation: Use only the latest live 402 response for supported chains, accepted payment terms, asset, payee, and price limits. <br>


## Reference(s): <br>
- [SIWX + x402 Reference](references/siwx-x402.md) <br>
- [Maestro documentation index](https://docs.gomaestro.org/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/Vardominator/maestro-skill) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with HTTP request details, headers, response summaries, and inline shell commands when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected network, payment amount, signer address, credit headers, and payment settlement metadata when returned by Maestro.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
