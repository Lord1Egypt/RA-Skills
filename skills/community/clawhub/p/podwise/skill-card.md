## Description:

Helps listeners discover, summarize, study, and organize podcasts and other audio using Podwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saitowu](https://clawhub.ai/user/saitowu)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast listeners use this skill to find and summarize episodes, review their listening history, create episode notes and study cards, and research topics across transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Podwise account connection exposes listening and reading history and followed shows.

Mitigation: Connect only if comfortable sharing this account data through Podwise OAuth.

Risk: User-provided audio or video may be uploaded to Podwise for processing.

Mitigation: Review media contents and obtain consent before uploading.

Risk: Generated notes and listener profiles may be saved locally.

Mitigation: Review generated files, especially taste.md, before keeping or sharing them.

Risk: Optional headless setup may install mcp-remote without a pinned version.

Mitigation: Consider pinning or preinstalling mcp-remote before headless setup.

## Reference(s):

- [Podwise skill listing](https://clawhub.ai/saitowu/skills/podwise)
- [Podwise](https://podwise.ai)
- [Podwise connection and sign-in](artifact/references/installation.md)
- [Podwise tool reference](artifact/references/mcp.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown, text, and optional exported files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local listener profile or episode exports.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
