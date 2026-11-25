## Description:

Decides hand-vs-compiler for loop transforms (unrolling, SIMD, fusion, branchless)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when reviewing or authoring a profiled hot loop to decide whether a manual transformation is useful, redundant, or likely to hurt compiler optimization. It guides profiling, vectorization checks, and benchmarking on representative data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean scan does not establish that the skill is risk-free or that its recommendations fit a particular use case.

Mitigation: Review the skill instructions before use and confirm that its profiling and benchmarking guidance suits the loop and workload.

## Reference(s):

- [Project homepage (ClawHub metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [Branchless Rust performance reference](https://www.greyblake.com/blog/branchless-rust/)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations and examples are conditioned on language, compiler behavior, profiling results, and input distribution.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
