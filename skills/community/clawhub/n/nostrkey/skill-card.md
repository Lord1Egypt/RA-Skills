## Description: <br>
Cryptographic identity SDK for AI agents: generate Nostr keypairs, sign events, encrypt messages, BIP-39 seed phrases, and portable backup tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to create or restore a dedicated Nostr identity, sign Nostr events, encrypt direct messages, and manage encrypted identity backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to handle seed phrases and passphrases during identity setup. <br>
Mitigation: Use a fresh low-value Nostr identity, provide NOSTRKEY_PASSPHRASE through a secure environment secret, and avoid pasting important existing seed phrases into chat. <br>
Risk: Examples can sign events and publish to Nostr relays. <br>
Mitigation: Require explicit operator approval before signing or relay publishing, and review event content before execution. <br>
Risk: Example code includes a placeholder passphrase for saving an identity file. <br>
Mitigation: Replace placeholder passphrases with securely managed secrets before using the examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vveerrgg/nostrkey) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/vveerrgg) <br>
- [Project homepage](https://github.com/HumanjavaEnterprises/nostrkey.app.OC-python.src) <br>
- [PyPI package](https://pypi.org/project/nostrkey/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python code blocks and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces identity setup guidance, Nostr public-key details, encrypted identity files, and JSON public identity metadata when the examples are executed.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter, metadata.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
