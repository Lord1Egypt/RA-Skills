## Description:

Build and deploy OpenClaw as Docker images or portable packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfanmy](https://clawhub.ai/user/zfanmy)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to build Docker images and portable deployment packages for OpenClaw, then move clean or full variants to target servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full portable packages can include private configuration, tokens, and conversation history.

Mitigation: Prefer the clean package for sharing or deployment, audit package contents before transfer, and protect any full archive as sensitive data.

Risk: The Node.js installer uses a remote curl-to-bash installation path.

Mitigation: Use a verified Node.js installation method where possible and do not run the installer as root.

Risk: The build script recursively deletes the configured output directory before rebuilding packages.

Mitigation: Set OUTPUT_DIR to a deliberate disposable location and review it before running the build script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zfanmy/skills/openclaw-deploy)
- [Artifact README](artifact/README.md)
- [Portable template README](artifact/templates/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference clean and full deployment variants, Docker commands, portable package paths, and environment variables.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
