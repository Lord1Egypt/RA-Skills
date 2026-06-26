## Description: <br>
Run accuracy benchmarks when FlagEval is available and performance benchmarks with vLLM bench serve against a served model, covering five workload profiles and collecting throughput, latency, TTFT, and TPOT metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbavon](https://clawhub.ai/user/wbavon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to start a vLLM server in a benchmark container, run a standard profile matrix, and collect JSON and Markdown summaries of model serving performance. The current accuracy path reports FlagEval as skipped until a client is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs high-impact commands in a benchmark container. <br>
Mitigation: Install it only when the agent is expected to control that container, and run benchmarks in an isolated container without sensitive mounts. <br>
Risk: The vLLM server command enables remote model code execution by default. <br>
Mitigation: Use trusted, pinned model and tokenizer sources, and avoid --trust-remote-code for untrusted repositories. <br>
Risk: The documented stop command uses a broad process-kill pattern. <br>
Mitigation: Replace it with a tracked process ID or a dedicated disposable container before shared use. <br>


## Reference(s): <br>
- [Benchmark Profiles](references/benchmark-profiles.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wbavon/perf-test-flagos) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, JSON, Markdown] <br>
**Output Format:** [JSON report with a Markdown summary table and inline shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes per-profile JSON benchmark results when an output directory is configured; accuracy is reported as skipped until FlagEval is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
