## Description:

Diagnose, configure, generate, simulate, and report on NI Multisim circuits through the Multisim MCP server for installation, schematic generation, simulation, waveform analysis, and electronic design reporting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxy050208](https://clawhub.ai/user/yxy050208)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and electronics engineers use this skill to drive a local NI Multisim workflow through Multisim MCP, including setup checks, circuit planning, schematic generation, simulation, waveform analysis, and report production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can start Multisim and create circuit, raw data, CSV, plot, manifest, schematic, and report files in local work directories.

Mitigation: Use only a trusted local Multisim MCP server, keep the server on local stdio, choose explicit work directories, and review approval gates before allowing schematic generation or simulation runs.

Risk: Unrestricted simulator commands or direct command-line execution could exceed the normal circuit workflow.

Mitigation: Keep ordinary runs to the safe op, dc, ac, and tran command subset, and do not enable unsafe command paths unless the user explicitly requests trusted local security research and the server operator enabled it.

Risk: Generated reports or schematic probes can be misleading if treated as authoritative without validating simulation results.

Mitigation: Verify success status, point counts, expected numeric relationships, manifests, and measured data before reporting conclusions; flag estimated or unverified values.

Risk: Editing or saving circuits can overwrite user source designs.

Mitigation: Prefer separate output directories and save modified circuits to new paths unless the user explicitly approves overwriting a source design.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxy050208/skills/multisim-circuit-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown, Files]

**Output Format:** [Markdown guidance with inline PowerShell commands, SPICE netlists, configuration fragments, CSV/report file instructions, and simulation analysis notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference local circuit, raw data, CSV, plot, manifest, schematic image, and Markdown report files through the Multisim MCP workflow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
