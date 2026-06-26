## Description: <br>
Benchmarks free OpenCode Zen models by calling OpenCode endpoints, measuring response time and token throughput, and printing a Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[braveheartzjh](https://clawhub.ai/user/braveheartzjh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare available free OpenCode Zen models by latency, token usage, and tokens-per-second throughput. It is intended for lightweight benchmarking and report generation in an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The benchmark makes outbound requests to OpenCode endpoints during execution. <br>
Mitigation: Install and run only in environments where outbound requests to opencode.ai are allowed and expected. <br>
Risk: Benchmark results can vary with network conditions, model availability, service rate limits, or models that are no longer free. <br>
Mitigation: Treat generated rankings as point-in-time measurements and rerun benchmarks when comparing models for operational decisions. <br>


## Reference(s): <br>
- [OpenCode Zen API base endpoint](https://opencode.ai/zen/v1) <br>
- [OpenCode Zen documentation](https://opencode.ai/docs/zh-cn/zen) <br>
- [ClawHub skill page](https://clawhub.ai/braveheartzjh/opencode-model-benchmark) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/braveheartzjh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Analysis, API Calls] <br>
**Output Format:** [Markdown report printed to stdout with terminal summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports response time, prompt tokens, completion tokens, total tokens, tokens per second, status, and output previews; no report file is written.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
