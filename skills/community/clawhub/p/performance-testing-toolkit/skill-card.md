## Description:

Enterprise-grade performance testing toolkit supporting HTTP load testing, stress testing, benchmark testing, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to load test, stress test, benchmark, and report on APIs, web services, and applications. It supports configurable HTTP methods, headers, request bodies, concurrency levels, durations, and report formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sustained high-volume traffic to arbitrary URLs.

Mitigation: Use it only against systems you own or are explicitly authorized to assess, and begin with low concurrency and short durations.

Risk: Configured POST, PUT, or DELETE requests could affect production data.

Mitigation: Prefer non-mutating methods for production checks, or test against isolated environments and disposable data.

Risk: Dependency posture may require review before installation.

Mitigation: Review and pin dependencies before installing in managed or production environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/skills/performance-testing-toolkit)
- [Publisher Profile](https://clawhub.ai/user/kaiyuelv)
- [Packaged README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, YAML configuration, and JSON or HTML performance report outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include request counts, success rates, response-time statistics, throughput, and error summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
