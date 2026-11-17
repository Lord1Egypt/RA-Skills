## Description:

Generates shareable HTML and PNG cards from the Ciba/Iciba Daily Sentence API, with selectable layouts and QR codes for pronunciation audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwter](https://clawhub.ai/user/lwter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Iciba daily sentence data into social sharing cards, including vertical moments-style and horizontal postcard-style layouts with pronunciation QR codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer can make outbound web requests from the user's environment, including user-provided API and image URLs.

Mitigation: Use the default Iciba endpoint when possible, avoid untrusted --api-url or --input-json values, and run the renderer in a network-restricted sandbox for sensitive environments.

Risk: Dependency behavior may change because the artifact lists unpinned Python packages.

Mitigation: Prefer pinned dependency versions before production use and review dependency updates before deployment.

## Reference(s):

- [Iciba API Fields](artifact/references/iciba-api-fields.md)
- [ClawHub Skill Page](https://clawhub.ai/lwter/skills/nexus-ciba-wechat)
- [Publisher Profile](https://clawhub.ai/user/lwter)
- [Iciba Daily Sentence API](https://open.iciba.com/dsapi/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated HTML, PNG, JSON, and status files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Renderer outputs include an HTML card, PNG card, data JSON, and hero_source.txt indicating whether the image came from the API or fallback generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
