## Description:

Kannaka Eye helps agents run a local glyph viewer that classifies text, files, or raw bytes into SGA classes and renders multi-layer Fano-plane glyph visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to start and operate a local glyph visualization service for inspecting data geometry, exporting glyph PNG or JSON, and monitoring the Kannaka constellation when related services are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged launcher may execute server.js from outside the skill directory or fail when that file is absent.

Mitigation: Do not run ./scripts/eye.sh start until server.js is packaged inside the skill directory and the exact file has been reviewed.

Risk: The stop and status commands can affect unrelated local services on a shared port.

Mitigation: Use a dedicated port and verify the process identity before running stop or status on shared machines.

Risk: Flux publishing may send glyph event metadata off the local machine when FLUX_URL is enabled.

Mitigation: Leave FLUX_URL unset unless remote event publishing is intended and approved for the data being visualized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickflach/skills/kannaka-eye)
- [Publisher profile](https://clawhub.ai/user/nickflach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local HTTP/API outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The running viewer can export PNG files and glyph JSON client-side; optional Flux publishing is enabled only when FLUX_URL is set.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
