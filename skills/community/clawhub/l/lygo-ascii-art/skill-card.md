## Description:

LYGO ASCII Art Studio directs agents and users to a live web tool for converting photos into ASCII, text, and type art with export options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to route photo-to-ASCII requests to the LYGO ASCII Art Studio, where humans can load an image, tune character and rendering settings, and copy or export TXT/PNG output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends users to an external web page for photo processing.

Mitigation: Use the site only with images appropriate for that third-party service, or request an offline/local conversion script for private or sensitive images.

Risk: The package claims browser-local processing, but the reviewed evidence does not independently substantiate the no-upload behavior.

Mitigation: Treat the privacy claim as unverified unless the site behavior is independently reviewed or network activity is checked.

## Reference(s):

- [Lattice Registration](references/LATTICE.md)
- [Canonical LYGO ASCII Art Studio](https://eternalhaven.ca/lygo-ascii-art.html)
- [GitHub Pages Mirror](https://deepseekoracle.github.io/eternalhaven/lygo-ascii-art.html)
- [Excavationpro Mirror](https://deepseekoracle.github.io/Excavationpro/lygo-ascii-art.html)
- [Source Repository](https://github.com/DeepSeekOracle/eternalhaven)
- [Immutable Ledger](https://github.com/DeepSeekOracle/lygo-protocol-stack/blob/main/docs/network_builder/IMMUTABLE_ANCHORS.json)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-ascii-art)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with URLs, usage steps, and occasional shell commands for lattice verification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill routes users to an external web page for image conversion and may describe TXT or PNG export steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
