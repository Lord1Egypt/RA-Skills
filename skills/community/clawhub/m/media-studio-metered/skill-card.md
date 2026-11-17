## Description:

Media Studio Metered helps agents generate images, video, audio, and voice through SettleMesh's metered pay-per-render CLI workflow, including image-to-image, text-to-speech, durable output links, and object storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[structureintelligence](https://clawhub.ai/user/structureintelligence)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and builders use this skill to run and resell metered media generation without holding separate provider keys. It guides agents through finding current SettleMesh tool IDs, quoting costs, generating media, and storing or serving outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses a mutable global CLI that handles credentials, billing, media uploads, and storage operations.

Mitigation: Review before installing, prefer a pinned and verified settlemesh CLI version, and use a restricted API key with spending limits.

Risk: Metered renders and durable storage can create costs or long-lived media links.

Mitigation: Confirm costs before paid renders, quote before charging end users, choose retention deliberately, and require explicit confirmation before deleting stored objects.

Risk: The authenticated environment may expose unrelated secrets to CLI execution.

Mitigation: Run with only the required SETTLE_API_KEY and avoid exposing unrelated secrets in the environment.

## Reference(s):

- [Media Studio Metered on ClawHub](https://clawhub.ai/structureintelligence/skills/media-studio-metered)
- [StructureIntelligence Publisher Profile](https://clawhub.ai/user/structureintelligence)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the settlemesh CLI and SETTLE_API_KEY; generated media, billing, retention, and storage behavior depend on authenticated SettleMesh responses.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
