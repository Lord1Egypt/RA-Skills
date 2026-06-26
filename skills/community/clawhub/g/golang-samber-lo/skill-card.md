## Description: <br>
Helps agents use samber/lo in Go projects, including type-safe collection transforms, package selection, standard-library tradeoffs, and performance-aware guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill when adding or maintaining samber/lo usage in Go codebases. It helps choose between core lo helpers, parallel variants, mutable operations, lazy iterators, SIMD helpers, and Go standard library alternatives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose code edits, dependency changes, or go and git commands. <br>
Mitigation: Review proposed changes to source files, go.mod, go.sum, and git state before accepting or running them. <br>
Risk: Using lo/mutable can introduce in-place side effects and concurrency-safety issues. <br>
Mitigation: Use mutable helpers only after profiling confirms allocation pressure and after callers confirm the original slice is no longer needed. <br>
Risk: Using lo/parallel for small or I/O-bound workloads can add overhead and reduce control over cancellation and errors. <br>
Mitigation: Use lo/parallel only for large CPU-bound transforms; use errgroup or similar context-aware patterns for I/O fan-out. <br>
Risk: lo/it and lo/exp/simd have version or stability constraints. <br>
Mitigation: Confirm the module targets Go 1.23+ before using lo/it, and benchmark and pin versions before using experimental SIMD helpers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-samber-lo) <br>
- [Skill collection homepage](https://github.com/samber/cc-skills-golang) <br>
- [samber/lo GitHub repository](https://github.com/samber/lo) <br>
- [samber/lo documentation](https://lo.samber.dev) <br>
- [pkg.go.dev: github.com/samber/lo](https://pkg.go.dev/github.com/samber/lo) <br>
- [Package Guide](references/package-guide.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Go code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose source edits, dependency updates, and go or git commands for user review.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
