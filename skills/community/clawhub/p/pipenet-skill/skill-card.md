## Description:

Pipenet-skill helps agents design, solve, analyze, and visualize TOML-described fluid pipeline networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiderdking](https://clawhub.ai/user/spiderdking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create pipeline-network TOML configurations, run hydraulic solving and reliability analysis, and generate visualizations of network structure and operating state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles user-controlled TOML file paths and generated output paths.

Mitigation: Constrain file access to trusted working directories, reject arbitrary host paths, and prevent overwrites or path traversal before installation or use.

Risk: Generated HTML visualizations may include user-controlled network or scenario names.

Mitigation: Sanitize names used in HTML output and open generated visualization files in an isolated browser context until output validation and escaping are reviewed.

Risk: Untrusted TOML inputs can influence network topology, scenarios, and file generation behavior.

Mitigation: Use trusted TOML inputs only, validate network and scenario names, and review generated files before relying on the analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spiderdking/skills/pipenet-skill)
- [skill.md](artifact/skill.md)
- [skill.yaml](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [text, configuration, code, files, guidance]

**Output Format:** [Tool responses containing Python dictionaries, generated TOML configuration, analysis logs, and HTML visualization file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local TOML and HTML outputs when invoked with valid network inputs and paths.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.yaml, src/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
