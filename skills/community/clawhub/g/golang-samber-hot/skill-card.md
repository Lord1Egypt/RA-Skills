## Description: <br>
In-memory caching in Golang using samber/hot for eviction algorithms, TTL, cache loaders, sharding, stale-while-revalidate, missing key caching, and Prometheus metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when adopting or maintaining samber/hot caches in Go services. It helps select eviction algorithms, configure TTLs and loaders, size caches, prevent common runtime mistakes, and add production monitoring patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency update commands such as go get -u can change module versions beyond the cache library. <br>
Mitigation: Review go.mod and go.sum changes before accepting them, then run the project's normal tests and linting. <br>
Risk: Generated cache code or git operations may alter application behavior or repository state. <br>
Mitigation: Inspect proposed code and git changes before applying them, especially around TTLs, loaders, concurrency settings, and cache capacity. <br>


## Reference(s): <br>
- [samber/cc-skills-golang homepage](https://github.com/samber/cc-skills-golang) <br>
- [samber/hot package documentation](https://pkg.go.dev/github.com/samber/hot) <br>
- [samber/hot source repository](https://github.com/samber/hot) <br>
- [Algorithm Selection Guide](references/algorithm-guide.md) <br>
- [API Reference](references/api-reference.md) <br>
- [Production Patterns](references/production-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Go and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recommendations and implementation snippets for Go projects using samber/hot.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
