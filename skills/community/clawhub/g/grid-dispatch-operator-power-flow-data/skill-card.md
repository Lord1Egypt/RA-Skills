## Description:

Power system network data formats and topology. Use when parsing bus, generator, and branch data for power flow analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power systems engineers use this skill to understand MATPOWER-style network JSON data and parse buses, generators, branches, reserve fields, and load values for power flow analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example parsing code may process large user-provided network JSON files.

Mitigation: Run parsing locally only on files the user intentionally provides and use Python's JSON parser as the skill recommends.

Risk: Power-flow data interpretation can be incorrect if bus numbering is assumed to be contiguous.

Mitigation: Create an explicit bus-number-to-index mapping before joining buses, generators, and branches.

## Reference(s):

- [PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text guidance for local parsing of user-provided power network JSON files.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
