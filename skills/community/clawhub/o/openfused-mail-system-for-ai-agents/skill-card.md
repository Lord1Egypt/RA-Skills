## Description: <br>
Decentralized context mesh for AI agents that helps manage stores, send signed or encrypted messages, sync with peers, and manage cryptographic trust. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[velinxs](https://clawhub.ai/user/velinxs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up file-based context stores, exchange messages between trusted agent peers, synchronize shared context, and manage local cryptographic trust for an agent mesh. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Peer synchronization and messaging can transfer context or shared files to configured peers. <br>
Mitigation: Add only trusted peers, prefer encrypted recipients over plaintext delivery, and confirm the target store before syncing or sending messages. <br>
Risk: Files placed in the shared directory are plaintext and visible to synced peers. <br>
Mitigation: Keep sensitive files out of shared/ and review shared contents before sync. <br>
Risk: Autonomous watch or sync use can send or receive data without an immediate human prompt. <br>
Mitigation: Use watch mode only with confirmation and sandbox controls, especially in environments where agents may invoke skills autonomously. <br>
Risk: SSH-based peer sync uses the user's existing SSH configuration and trusted endpoints. <br>
Mitigation: Review ~/.ssh/config and peer URLs before adding peers or running sync. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/velinxs/openfused-mail-system-for-ai-agents) <br>
- [Openfused GitHub Repository](https://github.com/wearethecompute/openfused) <br>
- [openfused npm Package](https://www.npmjs.com/package/openfused) <br>
- [Publisher Profile](https://clawhub.ai/user/velinxs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agent use of the openfuse CLI and local mesh files; it does not itself generate private key material in the skill text.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata); artifact frontmatter version is 0.3.6 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
