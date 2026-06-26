## Description: <br>
Run HTTP performance tests with latency and throughput measurement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to benchmark HTTP services they own or are authorized to test, including latency, throughput, stress, report, and comparison checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark commands can create network load or target services without authorization. <br>
Mitigation: Run tests only against services you own or are explicitly authorized to test, and choose request counts and concurrency levels appropriate for the environment. <br>
Risk: Report and comparison commands read user-provided file paths. <br>
Mitigation: Pass only generated benchmark logs or other files you intend the agent to read. <br>
Risk: Shell-based benchmarking depends on user-supplied URLs and local curl behavior. <br>
Mitigation: Review target URLs and command arguments before execution, and run in a controlled shell environment. <br>


## Reference(s): <br>
- [Perftest on ClawHub](https://clawhub.ai/bytesagain-lab/perftest) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and stores benchmark data under ~/.local/share/perftest/.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
