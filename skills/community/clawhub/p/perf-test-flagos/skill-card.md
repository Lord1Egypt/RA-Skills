## Description:

Run accuracy benchmarks when FlagEval is available and performance benchmarks with vllm bench serve against a served model across five workload profiles, collecting throughput, latency, TTFT, and TPOT metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start or target a served vLLM model, run repeatable performance profiles, and produce JSON plus Markdown summaries for release or model validation. Accuracy testing is currently reported as skipped until a FlagEval client is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags that the skill can run untrusted model repository code and broad Docker shell commands.

Mitigation: Review before installing or running, and execute only in a dedicated, unprivileged benchmark container without sensitive mounts, credentials, Docker socket access, or privileged mode.

Risk: The benchmark flow may use trust-remote-code for model execution.

Mitigation: Do not use trust-remote-code unless the model repository and exact revision have been vetted.

Risk: Command parameters may be supplied by a user or release workflow.

Mitigation: Validate or quote all user-supplied command parameters before execution.

## Reference(s):

- [Benchmark Profiles](references/benchmark-profiles.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON report structure, and Markdown summary table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces benchmark status, per-profile metrics, accuracy skip status, and partial failure reporting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
