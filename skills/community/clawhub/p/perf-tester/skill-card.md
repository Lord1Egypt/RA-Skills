## Description:

Performance and load testing for APIs and web services: designs test scenarios, generates k6, Locust, and JMeter scripts, analyzes response times, throughput, and error rates, and identifies bottlenecks using industry-standard methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to plan load, stress, spike, soak, scalability, and baseline tests for APIs and web services, then generate executable test scripts and interpret latency, throughput, error-rate, and Apdex results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated performance tests can create real traffic against a target system.

Mitigation: Run generated tests only against systems you own or are explicitly authorized to test, preferably in staging or isolated environments.

Risk: High load levels can disrupt services or exceed approved capacity.

Mitigation: Keep initial load conservative and increase only after capacity, monitoring, and approvals are clear.

Risk: Test scripts may require credentials for protected endpoints.

Mitigation: Use short-lived test credentials and avoid embedding secrets directly in generated scripts or shared reports.

Risk: Generated scripts may rely on external tooling or libraries.

Mitigation: Pin or vendor dependencies where possible and review generated commands before execution.

## Reference(s):

- [k6 Advanced Patterns](references/k6-patterns.md)
- [Locust Distributed Mode](references/locust-distributed.md)
- [Grafana k6 documentation](https://grafana.com/docs/k6/latest/)
- [Install k6](https://grafana.com/docs/k6/latest/set-up/install-k6/)
- [Locust documentation](https://docs.locust.io/en/stable/)
- [Locust distributed mode](https://docs.locust.io/en/stable/running-distributed.html)
- [Apdex Alliance Specification](http://apdex.org/specs.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JavaScript, Python, YAML, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated performance-test scripts, run commands, thresholds, metrics tables, and recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
