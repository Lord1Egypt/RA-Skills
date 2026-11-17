## Description:

Lumi Diary collects life fragments and stitches them into interactive local memory scrolls while storing journals, portraits, media, keepsakes, and exported capsules on the user's device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thhoho](https://clawhub.ai/user/thhoho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Lumi Diary as a local-first memory assistant for personal journaling, group-chat memory capture, event storytelling, and portable memory exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently records personal and group-chat memories, contact identifiers, personality impressions, milestones, and media.

Mitigation: Use it only where participants know Lumi is present, and periodically review or delete stored fragments, portraits, keepsakes, and media from the local vault.

Risk: Local media path handling can expose sensitive files if the agent is given arbitrary paths.

Mitigation: Provide only intended media files, keep the vault scoped with LUMI_VAULT_PATH, and avoid pointing the skill at unrelated local directories.

Risk: Exported and imported .lumi capsules can contain sensitive memory data and should be treated as untrusted archives.

Mitigation: Review capsule contents before sharing, import capsules only from trusted sources, and inspect imported memories after merging.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thhoho/skills/lumi-diary)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, files, configuration]

**Output Format:** [Conversational text plus local Markdown and JSON records, HTML memory scrolls, .lumi ZIP capsules, and optional PNG exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores data in a local Lumi_Vault directory and can use LUMI_VAULT_PATH to select the vault location.]

## Skill Version(s):

0.2.0 (source: server release, SKILL.md frontmatter, pyproject.toml, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
