## Description:

Decides hand-vs-compiler for loop transforms (unrolling, SIMD, fusion, branchless).

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when reviewing or writing a profiled hot loop to decide whether a manual transformation is likely to help, and how to validate a speedup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loop changes judged from synthetic or unrepresentative benchmarks may be slower on production data.

Mitigation: Profile first and compare performance on representative production-distribution data before claiming a speedup.

Risk: Branchless rewrites can increase memory use and make loop logic harder to maintain, especially when branch outcomes are predictable or selectivity is skewed.

Mitigation: Check production selectivity and allocation costs, and compare against the ordinary branch on representative inputs before adopting the rewrite.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-loop-optimization)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [Branchless Rust performance example](https://www.greyblake.com/blog/branchless-rust/)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
