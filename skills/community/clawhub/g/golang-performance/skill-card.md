## Description: <br>
Golang Performance helps agents diagnose Go performance bottlenecks and choose optimization patterns for allocations, CPU efficiency, memory layout, garbage collection, pooling, caching, and hot paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when profiling or benchmarks identify a Go performance bottleneck, or when reviewing Go code for likely allocation, CPU, memory, runtime, caching, I/O, or observability improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence marks the release as suspicious and advises review before enabling it outside a trusted maintainer environment. <br>
Mitigation: Review the skill and allowed tools before installation, enable it only in trusted workspaces, and use stricter sandboxing or reduced tool authority where available. <br>
Risk: Performance recommendations or code edits can degrade correctness, shift bottlenecks, or produce misleading gains if applied without measurement. <br>
Mitigation: Require profiling, tests, baseline benchmarks, one change at a time, and benchstat comparison before relying on any proposed optimization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-performance) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [Caching Patterns](references/caching.md) <br>
- [CPU Optimization](references/cpu.md) <br>
- [I/O & Networking Optimization](references/io-networking.md) <br>
- [Memory Optimization](references/memory.md) <br>
- [Production Observability for Performance](references/observability.md) <br>
- [Runtime Tuning](references/runtime.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Go code examples, shell commands, and optional YAML configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations should be validated with profiling, tests, benchmarks, and benchstat comparisons before adoption.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
