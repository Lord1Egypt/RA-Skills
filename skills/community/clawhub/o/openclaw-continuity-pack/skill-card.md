## Description:

Installs reusable OpenClaw workspace continuity templates and an optional full continuity route for same-thread rollover, hidden handoff, and silent continuity preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buasakaking](https://clawhub.ai/user/buasakaking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to scaffold portable workspace continuity templates, install memory/plans/status/handoff workflows, or check and apply a runtime continuity patch in a matching OpenClaw source tree.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace installation can add broad persistent agent rules, continuity conventions, and automatic memory behavior.

Mitigation: Review the files that will be added before installation and prefer the continuity-only route when the broader operating layer is not needed.

Risk: The example configuration may include high-privilege settings that are unsafe in sensitive environments.

Mitigation: Do not copy the example configuration directly; configure models, API endpoints, secrets, and execution permissions explicitly for the target environment.

Risk: The full continuity route changes a matching OpenClaw source tree and requires rebuilding runtime and UI assets.

Mitigation: Use a test environment first, back up affected install/workspace paths, run the patch check before applying, rebuild both runtime and UI assets, and follow the rollback notes if verification fails.

Risk: The provided artifact references a runtime patch file, but the file is absent from the artifact copy inspected here.

Mitigation: Treat the missing runtime patch as a blocker for the full continuity route until the expected patch file is present and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/buasakaking/skills/openclaw-continuity-pack)
- [Overview](references/overview.md)
- [Install](references/install.md)
- [Usage](references/usage.md)
- [Capability Layers](references/capability-layers.md)
- [Verify](references/verify.md)
- [Rollback](references/rollback.md)
- [Upgrade Maintenance](references/upgrade-maintenance.md)
- [Source Audit](references/source-audit.md)
- [Changelog](references/changelog.md)
- [Release Notes](references/release-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and references to bundled scripts, templates, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent may recommend or run bundled Python scripts that write workspace files or check/apply a patch when the operator chooses that route.]

## Skill Version(s):

0.5.0 (source: server release evidence and references/changelog.md, released 2026-04-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
