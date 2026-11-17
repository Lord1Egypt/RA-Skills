## Description:

Compares two registered Multisim experiments by reviewing circuit topology, settings, measurements, validation results, and artifact hashes to explain baseline-versus-candidate changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxy050208](https://clawhub.ai/user/yxy050208)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare a baseline Multisim experiment with a candidate run, identify meaningful differences in topology, solver settings, measurements, verification status, and hashes, and call out when test conditions are not directly comparable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read more experiment artifact content than needed to explain a comparison.

Mitigation: Use bounded summaries first and read only the text artifact pages needed to explain the observed differences.

Risk: The agent may overstate causality or force a conclusion when experiment conditions are not comparable.

Mitigation: Distinguish design changes, solver-setting changes, sampling differences, and missing evidence, and explicitly mark incompatible conditions as not directly comparable.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown with compact comparison tables and concise findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include evidence references, likely causes, and unverified hypotheses; does not export binary artifacts unless explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
