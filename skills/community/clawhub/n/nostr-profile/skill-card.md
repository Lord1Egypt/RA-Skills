## Description: <br>
Nostr profile management for AI agents - publish, read, and update kind 0 metadata on any relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an agent create, publish, inspect, and update public Nostr kind 0 profile metadata through configured relays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nostr profile updates are public signed actions, so names, bios, and image URLs may expose information broadly. <br>
Mitigation: Review relay, name, bio, and image URLs before publishing, avoid private information, and prefer a dedicated Nostr identity. <br>
Risk: Publishing or updating a profile requires access to signing credentials. <br>
Mitigation: Do not provide signing secrets for read-only lookups, avoid displaying or logging private keys, and request passphrases only when signing is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vveerrgg/nostr-profile) <br>
- [Project homepage](https://github.com/HumanjavaEnterprises/huje.nostrprofile.OC-python.src) <br>
- [PyPI package](https://pypi.org/project/nostr-profile/) <br>
- [NostrKey prerequisite](https://clawhub.ai/vveerrgg/nostrkey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish, read, or update public Nostr profile metadata through configured relays when the agent executes the referenced Python package.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
