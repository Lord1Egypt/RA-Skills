## Description: <br>
A cryptographic protocol for AI agents to mint, sign, verify, and transfer SVG digital assets without a blockchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obekt](https://clawhub.ai/user/obekt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create portable SVG assets with embedded cryptographic provenance, verify ownership chains, and transfer assets between did:key identities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using SVG ownership as authorization for APIs, compute, credits, or paid resources can over-grant access without additional controls. <br>
Mitigation: Add scoped credentials, short lifetimes, revocation, replay protection, audit logging, and explicit user control before connecting verified SVGs to valuable resources. <br>
Risk: Demo key handling and access-token guidance need review before use with real assets. <br>
Mitigation: Do not use the demo vault for valuable keys; review secret storage and key-management behavior before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/obekt/nifty-agents-protocol) <br>
- [Project homepage](https://github.com/obekt/niftyagents) <br>


## Skill Output: <br>
**Output Type(s):** [Code, JSON, Shell commands, Guidance] <br>
**Output Format:** [TypeScript functions, REST JSON responses, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No required environment variables; optional local verification server accepts SVG input.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
