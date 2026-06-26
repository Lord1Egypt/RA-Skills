## Description: <br>
A buyer-side guide for verifying AI agent identity, auditing performance claims, and evaluating cryptographic reputation signals with GreenHelix API examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, enterprises, and agent operators use this skill to evaluate whether another AI agent is trustworthy before sharing data, delegating work, or committing funds. It provides due-diligence patterns for identity checks, verified metrics, Merkle claim chains, reputation scores, escrow history, disputes, and continuous monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide includes runnable examples that can create escrow contracts and lock funds if copied into an autonomous workflow. <br>
Mitigation: Use sandbox or test defaults first, require explicit human approval for escrow creation, and apply spending limits before any production use. <br>
Risk: The skill references sensitive credentials, including a GreenHelix API key and an agent signing key. <br>
Mitigation: Use least-privilege credentials and avoid providing a real signing key unless the specific workflow requires it. <br>
Risk: The security verdict is suspicious even though the artifact is described as a non-executable educational guide. <br>
Mitigation: Treat the examples as reference material, review each API action before running it, and do not copy escrow or hiring examples into an agent without human approval. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mirni/greenhelix-agent-trust-verification) <br>
- [GreenHelix sandbox API endpoint](https://sandbox.greenhelix.net) <br>
- [GreenHelix API reference and tool catalog](https://api.greenhelix.net/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples reference GREENHELIX_API_KEY and AGENT_SIGNING_KEY.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
