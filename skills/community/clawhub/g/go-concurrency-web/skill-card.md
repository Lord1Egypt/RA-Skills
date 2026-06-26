## Description: <br>
Go concurrency patterns for high-throughput web applications including worker pools, rate limiting, race detection, and safe shared state management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design and review concurrent Go web services, especially worker pools, rate limiters, race-detector checks, and safe shared-state handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example snippets may be unsuitable as direct production code without project-specific adaptation, especially around context cancellation and shutdown behavior. <br>
Mitigation: Review the pattern in the target service, adapt it to the service lifecycle, and run the relevant Go tests or builds before deployment. <br>
Risk: Race-detector commands execute project tests or builds and may be inappropriate in restricted environments without approval. <br>
Mitigation: Run `go test -race` or `go build -race` only in approved local or CI environments where executing the project code is acceptable. <br>


## Reference(s): <br>
- [Worker Pools](references/worker-pools.md) <br>
- [Rate Limiting](references/rate-limiting.md) <br>
- [Race Detection](references/race-detection.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/go-concurrency-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Go and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; examples should be adapted and reviewed before production use.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
