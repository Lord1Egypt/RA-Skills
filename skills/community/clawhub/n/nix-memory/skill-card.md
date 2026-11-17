## Description:

nix-memory provides Bash-based identity hashing, memory integrity checks, drift detection, and continuity scoring for OpenClaw agent workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassh100k](https://clawhub.ai/user/cassh100k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to baseline identity and memory files, detect unexpected drift, and review continuity signals across OpenClaw sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer guidance includes remote shell execution patterns.

Mitigation: Prefer reviewed local scripts from the package and avoid curl-to-bash installation.

Risk: Setup and quickstart can persist copies, hashes, diffs, logs, and helper files derived from private workspace memory files.

Mitigation: Run setup only in workspaces where .nix-memory state and generated helper files are acceptable, and review stored reports before sharing the workspace.

Risk: Heartbeat integration can add recurring memory checks to HEARTBEAT.md.

Mitigation: Inspect or edit HEARTBEAT.md after quickstart if recurring future execution is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cassh100k/skills/nix-memory)
- [nix-memory documentation](https://nixus.pro/memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Shell status text, Markdown guidance, JSON reports, and workspace configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates workspace state under .nix-memory and may create heartbeat, memory, and agent discovery files when quickstart is run.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
