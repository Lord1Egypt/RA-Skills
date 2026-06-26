## Description: <br>
Social awareness for AI entities -- contacts, trust tiers, and identity verification over Nostr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to give agents Nostr-based contact awareness, trust tiers, identity verification workflows, and social-graph maintenance guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance may expose the root device secret if it is printed, pasted, or logged. <br>
Mitigation: Store the device secret in a secure secret manager or encrypted backup, and avoid printing, pasting, or logging it. <br>
Risk: The skill manages identity-linked relationship data and uses Nostr private key or passphrase material. <br>
Mitigation: Protect Nostr private keys and passphrases, review the external Python package before providing credentials, and only install in environments where this data handling is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vveerrgg/nostrsocial) <br>
- [NostrSocial homepage](https://github.com/HumanjavaEnterprises/nostrsocial.app.OC-python.src) <br>
- [NostrSocial on PyPI](https://pypi.org/project/nostrsocial/) <br>
- [NostrKey prerequisite](https://clawhub.ai/vveerrgg/nostrkey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup guidance for sensitive Nostr keys, passphrases, contact data, and relationship-state persistence.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
