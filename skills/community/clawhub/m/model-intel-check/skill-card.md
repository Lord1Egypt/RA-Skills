## Description:

Checks whether an OpenAI-compatible model API endpoint appears to be serving a full-strength reasoning model by running fixed benchmark protocols and comparing results with official reference anchors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2641183145-oss](https://clawhub.ai/user/2641183145-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate whether a proxy, relay, or upstream OpenAI-compatible endpoint is returning the expected model quality. It guides benchmark setup, execution, failure reruns, anti-cheat checks, and reporting for endpoint comparison or suspected model substitution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Hugging Face token may be sent while fetching gated benchmark data, including through an unofficial mirror path.

Mitigation: Use official data sources where possible, use a fine-grained read-only token, avoid running make_data.py with HF_TOKEN unless the mirror behavior is acceptable, and revoke the token after use.

Risk: Benchmark runs make outbound model API calls that may consume quota, incur cost, or hit rate limits.

Mitigation: Confirm the endpoint, model, and concurrency before running, monitor provider quota and billing, and lower concurrency or stop the run if errors increase.

Risk: Results written locally can include full model completions and benchmark details.

Mitigation: Run in a clean local directory, keep result files local unless reviewed, and avoid sharing benchmark data or completions that should remain private.

Risk: The local Web UI keeps a benchmark service running after launch.

Mitigation: Use the localhost UI only when needed and stop the service when the benchmark session is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2641183145-oss/skills/model-intel-check)
- [Benchmark reference anchors](references/README.md)
- [Benchmark suite catalog](references/benchmarks.md)
- [Anti-cheat and validation checks](references/anti-cheat.md)
- [Dataset preparation notes](data/README.md)
- [Kimi Vendor Verifier](https://github.com/MoonshotAI/Kimi-Vendor-Verifier)
- [DeepSeek R1](https://github.com/deepseek-ai/DeepSeek-R1)
- [OpenAI GPT-5](https://openai.com/index/introducing-gpt-5/)
- [Gemini models](https://deepmind.google/models/gemini/)
- [GPQA dataset](https://huggingface.co/datasets/Idavidrein/gpqa)
- [MathArena](https://matharena.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, local result files, and benchmark summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSONL result records, answer review text files, and optional localhost Web UI status output.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
