## Description: <br>
Use when the user asks to create, generate, build, audit, fix, compile, or look up smart contracts and tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[achilles1089](https://clawhub.ai/user/achilles1089) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to research tokens, generate smart contracts, audit contract code, fix findings, compile deployable artifacts, and prepare deployment guidance across supported blockchain networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Smart-contract outputs and deployment guidance can affect assets if used without review. <br>
Mitigation: Test on testnets first and get independent review before deploying contracts that will control real value. <br>
Risk: Token addresses, prompts, and submitted contract code are processed by Pentagonal tools or API calls. <br>
Mitigation: Install and use the skill only if you trust Pentagonal to process that information. <br>
Risk: Wallet private keys could be exposed if users paste them into chat. <br>
Mitigation: Do not paste private keys into chat; keep wallet keys in secure local tooling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/achilles1089/pentagonal) <br>
- [Deployment Guide](references/deployment.md) <br>
- [Example Conversation Flows](references/examples.md) <br>
- [Pentagonal Security Knowledge Base](references/security-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, deployment commands, and structured findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ABI, bytecode, constructor arguments, gas estimates, token intelligence, security findings, and deployment instructions when supported by the connected Pentagonal tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
