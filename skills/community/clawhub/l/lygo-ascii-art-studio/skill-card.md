## Description:

LYGO ASCII Art Studio directs agents and users to a live web tool for turning photos into ASCII, text, or type art, with lattice creative/tools anchors and companion links for related LYGO tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to route photo-to-ASCII requests to the LYGO ASCII Art Studio web page and provide brief operating instructions for converting images into text art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package points to an external web page for image conversion, and the no-upload privacy claim cannot be verified from the packaged files.

Mitigation: Use the external page only for images you are comfortable processing there; for sensitive photos, use a local/offline converter or independently inspect the web app first.

Risk: Generated art could be published to external services without the user's intent if an agent over-automates follow-up actions.

Mitigation: Require an explicit user yes before publishing generated art to GitHub, Hugging Face, social platforms, or other public destinations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-ascii-art-studio)
- [LYGO ASCII Art Studio](https://eternalhaven.ca/lygo-ascii-art.html)
- [GitHub Pages Mirror](https://deepseekoracle.github.io/eternalhaven/lygo-ascii-art.html)
- [Excavationpro Mirror](https://deepseekoracle.github.io/Excavationpro/lygo-ascii-art.html)
- [Project GitHub Link](https://github.com/DeepSeekOracle/eternalhaven)
- [Immutable Ledger](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/network_builder/IMMUTABLE_ANCHORS.json)
- [Lattice Registration](references/LATTICE.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown guidance with canonical URLs and concise user-facing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced web page can export text and PNG artifacts; this skill package itself provides routing and operating guidance.]

## Skill Version(s):

1.0.0 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
