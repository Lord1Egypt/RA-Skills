## Description: <br>
A local-first cryptographic toolkit that claims to execute zero-knowledge proof generation, circuit compilation via SnarkJS/ZoKrates, and formal verification analysis on local files without external API or cloud data transmission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenticio](https://clawhub.ai/user/agenticio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to request local cryptographic proof generation, circuit compilation, formal checks, and audit-style manifests for project files. Evidence security review says the current implementation returns placeholder success messages, so outputs should be treated as workflow scaffolding until backed by real proof and verification tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may present placeholder proof generation or formal-check results as if they were real security evidence. <br>
Mitigation: Treat generated proof, audit, and formal-check messages as non-authoritative until the scripts execute real tools and produce independently verifiable artifacts. <br>
Risk: The artifact claims SnarkJS and ZoKrates workflows, but scanner guidance says the implementation does not currently provide reliable cryptographic assurance. <br>
Mitigation: Require manual review of the local toolchain commands and output artifacts before using the skill for security, audit, or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agenticio/proof) <br>
- [Publisher profile](https://clawhub.ai/user/agenticio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with local command and file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local workspace files under ~/.openclaw/workspace/proof; current scripts produce placeholder status messages rather than verifiable cryptographic artifacts.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
