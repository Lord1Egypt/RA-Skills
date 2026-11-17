## Description:

ComfyUI logs report missing external tools; isolate host, config, and executable paths quickly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage Windows-hosted ComfyUI startup warnings for missing external executables and resolve the affected host-native configuration path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A same-named executable from the wrong host or environment could be selected.

Mitigation: Confirm the application runtime boundary and review the absolute executable path before applying any configuration change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/host-dependency-triage)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with diagnostic steps and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose JSON configuration path updates for reviewer approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
