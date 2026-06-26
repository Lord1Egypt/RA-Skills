## Description: <br>
Send local files, uploaded attachments, or URLs for e-signature with Nota Sign while handling credential setup, environment selection, file validation, signer collection, and Node.js runtime fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notasign](https://clawhub.ai/user/notasign) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect Nota Sign credentials, validate supported documents, gather signer names and emails, and initiate Nota Sign envelopes in PROD or UAT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads documents and signer details to Nota Sign. <br>
Mitigation: Install and use it only when the publisher is trusted and the user is authorized to send the documents and signer data to Nota Sign. <br>
Risk: Nota Sign credentials include a private signing key stored in plaintext configuration files. <br>
Mitigation: Prefer the home config, avoid committing or backing up the config, restrict permissions such as chmod 600, and rotate the key if the config may have been exposed. <br>
Risk: PROD and UAT use separate credential sets. <br>
Mitigation: When switching environments, collect and replace appId, appKey, userCode, and serverRegion for the target environment instead of only changing the environment field. <br>
Risk: The temporary runtime fallback can download node@20 and tsx from npm. <br>
Mitigation: Use an existing Node.js 18 or newer runtime when possible; allow the fallback only in environments where temporary npm downloads are acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/notasign/notasign) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Operator Guide](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns envelope ID and send summary on success; surfaces validation or API errors with the next required action on failure.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
