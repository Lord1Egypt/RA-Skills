## Description:

Saves web articles to a local Obsidian vault with image capture, Markdown conversion, YAML frontmatter, and appended user notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liz-npa](https://clawhub.ai/user/liz-npa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn a supplied article URL and optional comments into an Obsidian-ready Markdown note saved in a configured local or iCloud vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs may be sent through Jina.ai or captured through browser-visible content, including pages the user is logged into.

Mitigation: Use only public, non-sensitive article URLs unless the user explicitly accepts third-party retrieval and authenticated-page capture.

Risk: Internal, localhost, file, cloud metadata, private, paywalled, or tokenized links could expose sensitive content.

Mitigation: Avoid those URL classes and review the target URL before invoking the skill.

Risk: Weak URL, path, and download safeguards can increase network, disk, or local file placement risk.

Mitigation: Configure the vault path carefully and monitor disk and network use until URL allowlisting, private-network blocking, bounded downloads, and path containment are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liz-npa/skills/obsidian-save-article)
- [ClawHub publisher profile](https://clawhub.ai/user/liz-npa)
- [Jina.ai Reader endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes with YAML frontmatter, Obsidian callouts, local image references, and JSON returned by the image-download helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes article notes and images under the configured Obsidian vault path and stores local path configuration in the user's home directory.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
