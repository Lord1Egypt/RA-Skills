## Description:

Query musescore.com for sheet music search results, score and license metadata, and official download links from a shell using the fpx CLI through a signed-in browser tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and musicians use the skill to search MuseScore and retrieve score and license metadata or official download links from shell workflows through a paired browser tab.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had medium confidence and covered 66.7% of components, leaving a referenced script partly inspected.

Mitigation: Review the referenced helper script and its behavior before installing or running the skill.

## Reference(s):

- [MuseScore endpoints and query examples](artifact/references/endpoints.md)
- [JSON store extraction helper](artifact/references/extract-store.mjs)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ClawHub skill release](https://clawhub.ai/chrischall/skills/musescore-fpx)

## Skill Output:

**Output Type(s):** [JSON, Shell commands]

**Output Format:** [JSON search results, score metadata, and download URLs; shell commands for setup and queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [fpx resolves official download URLs but does not fetch score file bytes.]

## Skill Version(s):

1.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
