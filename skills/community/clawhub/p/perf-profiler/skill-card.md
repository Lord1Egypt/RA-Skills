## Description:

Profile and optimize application performance. Use when diagnosing slow code, measuring CPU/memory usage, generating flame graphs, benchmarking functions, load testing APIs, finding memory leaks, or optimizing database queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to measure application performance, identify CPU and memory bottlenecks, generate flame graphs, benchmark code paths or endpoints, load test APIs, and analyze database query performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste profiling and benchmarking commands may execute mutable third-party packages.

Mitigation: Review and adapt commands before running them, and prefer pinned tool versions or project lockfiles.

Risk: Profilers and load tests can affect availability or performance when run against systems without authorization.

Mitigation: Run profilers and load tests only in authorized development or staging environments.

Risk: CPU profiles, heap snapshots, and benchmark artifacts can expose sensitive implementation or runtime data.

Mitigation: Handle profile and heap artifacts like sensitive logs and limit where they are stored or shared.

Risk: The benchmark helper uses eval-style command execution that is unsafe for untrusted input.

Mitigation: Do not copy the eval-based helper into CI or workflows that accept untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/skills/perf-profiler)
- [hyperfine benchmarking tool](https://github.com/sharkdp/hyperfine)
- [wrk load testing tool](https://github.com/wg/wrk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce profiling, benchmarking, load testing, and database analysis guidance for Node.js, Python, Go, and common command-line tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
