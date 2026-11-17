## Description:

Web-first, publishable OpenClaw skill for OpenAI OAuth account switching, including first-run takeover, environment discovery, doctor checks, runtime inspection, slot management, dry-run validation, controlled switch experiments, rollback planning, and release-safe packaging without bundling live auth snapshots, logs, callbacks, or other machine-specific runtime data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amior1024](https://clawhub.ai/user/amior1024)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw administrators use this skill to install and operate a local web-first workflow for OpenAI OAuth account takeover, inspection, switching, rollback, and release-safe packaging. It supports first-run onboarding, runtime diagnostics, slot management, local usage rollups, and explicit dry-run checks before account-switching writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent local web service has high-impact OAuth and account-switching authority.

Mitigation: Run it only on a trusted single-user administrator machine, keep it bound to 127.0.0.1, and access it through an SSH tunnel.

Risk: Generated web credentials and OAuth profile files are sensitive and may expose account access if mishandled.

Mitigation: Do not reuse the generated password, rotate it after setup, keep OAuth profile files private, and avoid packaging callbacks, backups, token ledgers, logs, or runtime state.

Risk: The security evidence calls out insecure credential handling and an unreviewed external OAuth helper.

Mitigation: Review the skill carefully before installation and defer production use until credential storage, password rendering, path validation, HTML escaping, minimal environment passing, and OAuth helper packaging are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amior1024/skills/openai-auth-switcher-public)
- [Publisher Profile](https://clawhub.ai/user/amior1024)
- [Compatibility](references/compatibility.md)
- [Install and Runbook](references/install-and-runbook.md)
- [Security Model](references/security-model.md)
- [Runtime Discovery](references/runtime-discovery.md)
- [Packaging Policy](references/packaging-policy.md)
- [Web API Preview](references/web-api-preview.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown guidance with shell commands, JSON diagnostics, configuration paths, and local web workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reference local OpenClaw runtime paths and should treat OAuth profile files, generated credentials, callbacks, backups, and logs as secrets.]

## Skill Version(s):

0.3.1-preview (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
