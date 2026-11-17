## Description:

OpenClawMP guides agents through using the OpenClaw Marketplace to register, authenticate, browse and install assets, publish releases, and perform community actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[502399493zjw-lgtm](https://clawhub.ai/user/502399493zjw-lgtm)

### License/Terms of Use:

MIT

## Use Case:

External developers and agents use this skill to operate OpenClaw Marketplace workflows through guidance and the bundled CLI, including asset discovery, installation, publishing, authentication, and account or community actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can read local marketplace credentials.

Mitigation: Install and run it only in environments where the OpenClaw Marketplace registry and local credential access are trusted.

Risk: Install and uninstall commands can modify persistent agent asset directories.

Mitigation: Test in an isolated environment first and review the target asset and destination before allowing persistent changes.

Risk: Publish commands can upload local directories that may contain secrets or unintended files.

Mitigation: Review publication directories for credentials, private files, and generated artifacts before publishing.

Risk: Custom API endpoints can receive marketplace credentials.

Mitigation: Use the default registry unless the alternate endpoint is intentionally trusted.

## Reference(s):

- [ClawHub asset page](https://clawhub.ai/502399493zjw-lgtm/skills/openclawmp)
- [OpenClaw Marketplace](https://openclawmp.cc)
- [API Reference](references/api.md)
- [Asset Type Guide](references/asset-types.md)
- [CLI README](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run CLI commands, call marketplace APIs, read local credentials, install marketplace assets, publish local directories, or perform account and community actions.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
