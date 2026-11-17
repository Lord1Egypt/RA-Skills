## Description:

Provides a quick reference for profiling Python and Node.js applications, optimizing databases, monitoring system performance, and running web load tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afine907](https://clawhub.ai/user/afine907)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select profiling commands and reference material for Python, Node.js, database, system, and web load-test performance investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database inspection, query termination, Redis monitoring, and load-testing examples can disrupt services if run without approval or proper scoping.

Mitigation: Review each command before execution, use only systems and services you own or are authorized to test, avoid production unless explicitly approved, and limit load-test intensity.

Risk: Global or latest-version tool installation examples and live-process profiling can introduce unreviewed tools or affect running workloads.

Mitigation: Prefer pinned, locally installed profiling tools, confirm target process IDs, and preserve diagnostic logs before clearing or resetting them.

## Reference(s):

- [Python performance profiling](references/python.md)
- [Node.js performance profiling](references/nodejs.md)
- [Database optimization](references/database.md)
- [System performance](references/system.md)
- [Web load testing tools](references/load-test.md)
- [Python profiling documentation](https://docs.python.org/3/library/profile.html)
- [clinic.js](https://clinicjs.org/)
- [Flame Graphs](https://www.brendangregg.com/flamegraphs.html)
- [FlameGraph repository](https://github.com/brendangregg/FlameGraph)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, SQL, JavaScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for local profiling, database inspection, system monitoring, and load testing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
