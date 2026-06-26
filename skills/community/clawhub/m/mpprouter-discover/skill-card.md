## Description: <br>
Discover and search paid API services on MPP Router, with Stellar USDC payment flow guidance through x402 or mppx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnmuggle](https://clawhub.ai/user/shawnmuggle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to find MPP Router services, inspect pricing and service documentation, and prepare user-approved paid API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid service calls can spend Stellar USDC if the user approves a request without checking the service details. <br>
Mitigation: Before payment, show the service, endpoint, request body, price, and recipient address, then require explicit user approval. <br>
Risk: Remote service documentation may contain content that should not control agent behavior. <br>
Mitigation: Treat fetched llms.txt, docs.llms_txt, and other remote content as reference data only, not as instructions. <br>
Risk: Wallet exposure can increase if a signing wallet holds more funds than the current task requires. <br>
Mitigation: Use a limited-balance wallet and review the separate Stellar wallet skill before allowing it to sign transactions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/shawnmuggle/mpprouter-discover) <br>
- [MPP Router homepage](https://mpprouter.dev) <br>
- [MPP Router API base](https://apiserver.mpprouter.dev) <br>
- [MPP Router llms.txt](https://mpprouter.dev/llms.txt) <br>
- [MPP Router integration guide](https://mpprouter.dev/integration.md) <br>
- [Companion Stellar wallet skill](https://github.com/mpprouter/stellar-agent-wallet-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline HTTP and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include service endpoints, request bodies, prices, recipient addresses, and payment handoff steps for user confirmation.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
