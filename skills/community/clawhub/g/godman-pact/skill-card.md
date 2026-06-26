## Description: <br>
PACT - Protocol for Agent Constitutional Trust is a five-chamber agent-to-agent trust and negotiation protocol for identity verification, intent analysis, constitutional negotiation, capability-locked session tokens, and audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skingem1](https://clawhub.ai/user/skingem1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when two agents from different systems need to establish trust before data exchange, payment, or session creation. It guides first-contact trust negotiation, capability declaration, constitutional constraints, and secure session setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review verdict is suspicious because the release evidence flags elevated authority in a review helper. <br>
Mitigation: Install only in trusted repository contexts, review proposed commands before writes, use intended authenticated accounts, and avoid full sandbox bypass unless it is explicitly needed. <br>
Risk: PACT sessions are sensitive because they establish trust, payment terms, capability limits, and session tokens between agents. <br>
Mitigation: Preserve SOUL or other safety constraints, reject low-trust sessions, apply capability-locked tokens with expiry, and retain audit trails for review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/skingem1/godman-pact) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with protocol steps, tables, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe trust score bands, session ceilings, capability-locked token setup, and audit trail considerations.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
