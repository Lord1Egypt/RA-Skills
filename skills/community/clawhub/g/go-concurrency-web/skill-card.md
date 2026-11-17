## Description:

Go concurrency patterns for high-throughput web applications including worker pools, rate limiting, race detection, and safe shared state management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to apply Go concurrency patterns in web applications, including bounded worker pools, rate limiting, race detection, and safe shared state handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adopted concurrency examples can change application behavior through worker counts, queue sizes, background work, and shutdown paths.

Mitigation: Review sizing, backpressure, context propagation, and graceful teardown against the target service before merging generated changes.

Risk: Rate-limiting examples involving IPs, proxy headers, users, or API keys can be misapplied if trust boundaries or secret handling are wrong.

Mitigation: Trust forwarded headers only behind a controlled reverse proxy, protect API keys, and validate limiter keys and tiers during code review.

Risk: Race-detector output can miss logical races, deadlocks, starvation, or races not exercised by tests.

Mitigation: Pair race-detector runs with targeted concurrent tests and code inspection for synchronization, cancellation, and shared mutable state.

## Reference(s):

- [Worker Pools](references/worker-pools.md)
- [Rate Limiting](references/rate-limiting.md)
- [Race Detection](references/race-detection.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Go, shell, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes review gates and examples that should be adapted to the target service.]

## Skill Version(s):

2.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
