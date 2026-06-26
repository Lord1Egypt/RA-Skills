## Description: <br>
Lobster Distill packages, encrypts, uploads, and relays skill transfer instructions so one agent can share a skill with another through a human-forwarded message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiaoy01](https://clawhub.ai/user/qiaoy01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to transfer local skill directories or files between agents through a human relay, including across messaging platforms that only carry plain text. The workflow is intended for selected skill packages and requires the sender and receiver to review the transfer details before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The share workflow can upload selected local files to a third-party temporary file host. <br>
Mitigation: Verify the exact source path and contents before sharing, and avoid packaging secrets or unrelated files. <br>
Risk: The receive workflow can install archives received from another party with limited safety checks. <br>
Mitigation: Use only trusted senders, verify the URL, password, and expected package name, and inspect the decrypted archive before extraction. <br>
Risk: The relay note includes shell commands that download, decrypt, extract, and clean up files. <br>
Mitigation: Review commands before execution and run them only in an appropriate workspace or sandbox. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qiaoy01/lobster-distill) <br>
- [Publisher profile](https://clawhub.ai/user/qiaoy01) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style relay note with inline bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated relay note includes a download URL, decryption password, expiry notice, and receive/install commands.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
