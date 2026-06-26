## Description: <br>
Decentralized Identity (DID) and Verifiable Credentials management for AI Agents <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agent builders use this skill to create and manage decentralized identifiers, issue and verify W3C-style verifiable credentials, and evaluate agent trust relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles persistent decentralized-identity keys and verifiable credentials that can become sensitive secret material. <br>
Mitigation: Protect the ~/.openclaw/identity/ directory and avoid exposing private keys, credentials, or exported identity data. <br>
Risk: Installing or running an unexpected package source could execute code outside the intended Identity Trust release. <br>
Mitigation: Verify the npm or GitHub package source before installation or execution. <br>
Risk: Creating DIDs, issuing credentials, evaluating trust, or exporting identity data can change or disclose identity state. <br>
Mitigation: Require explicit confirmation before performing identity-changing or data-exporting actions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ZhenStaff/identity-trust) <br>
- [GitHub repository](https://github.com/ZhenRobotics/openclaw-identity-trust) <br>
- [Full documentation](https://github.com/ZhenRobotics/openclaw-identity-trust#readme) <br>
- [Quick Start Guide](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/QUICKSTART.md) <br>
- [API Reference](https://github.com/ZhenRobotics/openclaw-identity-trust/blob/main/src/types.ts) <br>
- [npm package](https://www.npmjs.com/package/openclaw-identity-trust) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript examples, and JSON-like DID or credential data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or operate on sensitive local identity material, including DIDs, credentials, trust scores, and key-storage paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
