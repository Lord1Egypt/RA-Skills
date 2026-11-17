## Description:

AI-powered meme generation, meme editing, and meme video generation for projects, powered by memelord.com's trending memetic data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamjasonlevin](https://clawhub.ai/user/iamjasonlevin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate, edit, download, and share image or video memes through the Memelord API. It supports scripted meme creation, asynchronous video render polling, and webhook signature verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, template data, generated media metadata, and API-backed requests are sent to memelord.com.

Mitigation: Use the skill only with a trusted Memelord account and avoid sending confidential or sensitive content.

Risk: Credential handling relies on MEMELORD_API_KEY and optional local `.env` loading.

Mitigation: Create your own `.env` or environment variables, keep file permissions restricted, and never use `.env` files from untrusted sources.

Risk: Webhook secrets and downloaded media URLs can be exposed or mishandled when passed through shell commands and output files.

Mitigation: Prefer secure secret handling, avoid storing secrets in shell history, and treat returned URLs and downloaded media paths as untrusted unless you control them.

## Reference(s):

- [Memelord homepage](https://memelord.com)
- [Memelord API documentation](https://www.memelord.com/docs)
- [ClawHub skill page](https://clawhub.ai/iamjasonlevin/skills/memelord)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell command examples, JSON response files, and generated media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEMELORD_API_KEY and local node, curl, and realpath binaries.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
