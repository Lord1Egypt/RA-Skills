## Description: <br>
Use this skill when an agent needs to pay for an x402 URL, transfer USDC, inspect OmniClaw balances or ledger entries, or explicitly expose an owner-approved paid endpoint through omniclaw-cli serve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abiorh001](https://clawhub.ai/user/abiorh001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide policy-controlled OmniClaw CLI payment workflows, balance and ledger inspection, x402 payments, USDC transfers, and owner-approved paid endpoint exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide spending or transfers through omniclaw-cli and requires sensitive credentials. <br>
Mitigation: Use least-privilege OMNICLAW_TOKEN values with spending limits, check policy with can-pay or simulate before new payments, and never print or store tokens in generated files. <br>
Risk: The optional OMNICLAW_OWNER_TOKEN can grant owner approval authority. <br>
Mitigation: Set OMNICLAW_OWNER_TOKEN only when the current task explicitly requires owner approval authority and stop for owner review when approval is required but authority was not intentionally granted. <br>
Risk: omniclaw-cli serve starts a network-accessible service and --exec runs a host command. <br>
Mitigation: Use serve or --exec only after explicit owner approval of the endpoint, price, command, port, and runtime isolation, preferably inside an isolated runtime. <br>
Risk: A malicious or untrusted OmniClaw Financial Policy Engine URL could expose financial workflow data or misdirect execution. <br>
Mitigation: Install only when the omniclaw-cli binary and OMNICLAW_SERVER_URL are trusted, and use scoped tokens for the intended wallet and policy. <br>


## Reference(s): <br>
- [OmniClaw CLI Reference](references/cli-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/abiorh001/omniclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and CLI workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference required environment variables, scoped credentials, payment checks, and owner approval conditions.] <br>

## Skill Version(s): <br>
0.0.8 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
