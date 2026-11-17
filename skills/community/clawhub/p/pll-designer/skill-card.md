## Description:

Calculates and analyzes phase-locked loop (PLL) PI controller parameters for power electronics and renewable energy workflows, supporting both target-bandwidth-to-PI design and PI-parameter-to-bandwidth analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncepuee](https://clawhub.ai/user/ncepuee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to tune SRF-PLL PI controller parameters, estimate PLL bandwidth, and check damping behavior for electrical grid and converter designs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PLL tuning results may be incorrect or misleading when system voltage, grid frequency, or damping ratio are assumed for a different operating context.

Mitigation: Confirm Unom, grid frequency, and damping ratio explicitly before relying on the calculated PI parameters or bandwidth, especially outside 690 V or 50 Hz systems.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with formulas and MATLAB-oriented code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks for missing critical electrical parameters before calculation and may state defaults for grid frequency and damping ratio when they are not provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
