## Description: <br>
A P2P encrypted social relationship management skill for friend discovery, relationship management, secure messaging, and social graph workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to discover peers, add and manage trusted friends, exchange encrypted messages, and inspect local social graph state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local peer discovery, key exchange, encrypted messaging, sync, and file sharing can expose sensitive relationship or message metadata if enabled unintentionally. <br>
Mitigation: Require explicit user confirmation before discovery, adding friends, messaging, sync, or file sharing, and review local storage and privacy settings before use. <br>
Risk: The release guidance notes a missing installer and a dependency on secure-p2p-messenger. <br>
Mitigation: Review the dependency and any installer before running install commands, and install only from inspected files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/lobster-friends-protocol-real) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local peer discovery, key exchange, SQLite metadata, encrypted messaging, sync, and file-sharing workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
