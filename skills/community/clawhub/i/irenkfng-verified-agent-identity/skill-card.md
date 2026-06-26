## Description: <br>
Billions decentralized identity for agents links agents to human identities using Billions ERC-8004 and Attestation Registries, verifies and generates authentication proofs, and is based on the iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[idraniw29](https://clawhub.ai/user/idraniw29) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage decentralized agent identities, link an agent DID to a human owner, sign authentication challenges, and verify DID ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles persistent identity keys and authentication material. <br>
Mitigation: Do not paste private keys, JWTs, or reusable identity tokens into commands or chat; configure encryption or a secret store before creating real identities. <br>
Risk: Human-agent linking is a persistent identity action. <br>
Mitigation: Confirm the DID, challenge, requester, registry destination, and agent name before running a linking command. <br>
Risk: The artifact documents Node.js scripts, but the release artifact contains only the skill instructions. <br>
Mitigation: Install only if you are prepared to review or supply the referenced scripts before executing identity workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/idraniw29/irenkfng-verified-agent-identity) <br>
- [Billions Network](https://billions.network/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON or text command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or use local identity data under $HOME/.openclaw/billions when the referenced scripts are present.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
