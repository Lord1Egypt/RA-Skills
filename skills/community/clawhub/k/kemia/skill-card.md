## Description:

Connect your OpenClaw instance to kemia for visual agent configuration management, including connection setup, deploy-ready config import, status checks, and one-time web login links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cwendler](https://clawhub.ai/user/cwendler)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an OpenClaw workspace to a trusted kemia deployment, export agent configuration files, import deploy-ready snapshots, and check connection or deployment status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote kemia server can influence local workspace files during import.

Mitigation: Only connect to a kemia server you control or strongly trust, and review deploy-ready snapshots before running import.

Risk: Agent configuration files and API credentials may be exposed to an arbitrary or untrusted URL.

Mitigation: Avoid plain HTTP, verify the base URL before connecting, and treat config.json and generated login links as secrets.

Risk: Imported filenames from the server may overwrite more than the intended agent markdown files.

Mitigation: Review server behavior and imported file lists before deployment; rely on the built-in backup as recovery, not as the primary control.

## Reference(s):

- [kemia API v1 Reference](artifact/references/api.md)
- [kemia service](https://kemia.byte5.ai)
- [ClawHub skill release page](https://clawhub.ai/cwendler/skills/kemia)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell command references and generated URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local workspace configuration and markdown files when the user runs the bundled scripts.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
