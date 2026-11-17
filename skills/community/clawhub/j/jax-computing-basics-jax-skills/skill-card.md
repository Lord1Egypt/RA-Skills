## Description:

High-performance numerical computing and machine learning workflows using JAX, including array operations, automatic differentiation, JIT compilation, RNN-style scans, map/reduce operations, and gradient computations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate JAX-oriented code and guidance for loading and saving numerical arrays, elementwise mapping, reductions, gradient computation, RNN-style scans, and JIT-compiled execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saving arrays writes to the caller-provided path and may replace an existing .npy file.

Mitigation: Review output paths before execution and avoid sensitive, ambiguous, or shared locations.

Risk: Loading local .npy or .npz files depends on the data supplied by the caller.

Mitigation: Use known numerical data files and validate shapes and types before running downstream JAX operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Code, Guidance, Markdown]

**Output Format:** [Markdown with Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include examples for local file loading and saving with .npy or .npz array data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
