## Description:

Share anonymized OpenClaw configurations with the OpenSoul community for sharing agent setups, discovering community examples, and finding inspiration for new capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fnaser](https://clawhub.ai/user/fnaser)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to register with OpenSoul, preview and share anonymized OpenClaw workspace profiles, browse or import community profiles for inspiration, and manage their shared entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anonymized workspace sharing may still miss secrets or private operating details.

Mitigation: Preview the generated output before sharing, avoid using the skill on workspaces that contain credentials or private memories, and remove any sensitive content before upload.

Risk: The OpenSoul API key is stored in a local credentials file and could be reused if exposed.

Mitigation: Protect the local credentials file and rotate the OpenSoul API key if the file may have been disclosed.

Risk: Imported community profiles may contain untrusted instructions or patterns.

Mitigation: Treat imported files as reference material only and review them before allowing an agent to use or follow their contents.

## Reference(s):

- [OpenSoul API Reference](references/api.md)
- [OpenSoul Schema Reference](references/schema.md)
- [OpenSoul Website](https://opensoul.cloud)
- [OpenSoul ClawHub Skill Page](https://clawhub.ai/fnaser/skills/opensoul-cloud)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands can print human-readable text or JSON, write imported profile files locally, and upload summarized profile data when sharing is confirmed.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
