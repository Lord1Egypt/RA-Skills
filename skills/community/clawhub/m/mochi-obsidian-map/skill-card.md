## Description:

Map Markdown wikilinks, backlinks, orphan notes and broken or ambiguous targets without changing the vault. Use for Obsidian Vault Link Map.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Obsidian users and developers can map links in a selected Markdown vault, find backlinks and orphan notes, and identify broken or ambiguous targets without editing notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports retain note names and link relationships, which may reveal private information about a vault.

Mitigation: Treat generated reports as private and store them accordingly.

Risk: Analyzing an unintended directory could expose data outside the intended vault.

Mitigation: Select only the vault directory for analysis and keep the host sandbox enabled.

## Reference(s):

- [Action contract](artifact/references/input.md)
- [MochiLab](https://mochilab.bz)
- [Obsidian Vault Link Map on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-obsidian-map)

## Skill Output:

**Output Type(s):** [Analysis, Files, JSON, HTML]

**Output Format:** [JSON and HTML report files with a concise summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports cover Markdown wikilinks, backlinks, orphan notes, and broken or ambiguous targets; source notes are not modified.]

## Skill Version(s):

1.0.1 (source: release evidence, skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
