## Description:

Run llama.cpp benchmarks on GGUF models to measure prompt processing (pp) and token generation (tg) performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexhegit](https://clawhub.ai/user/alexhegit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to benchmark GGUF models with llama.cpp, compare prompt processing and token generation throughput, and record repeatable llama-bench results across CPU, CUDA, ROCm, and Vulkan backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benchmark script can automatically run a locally discovered llama-bench executable.

Mitigation: Provide or verify a trusted llama-bench path before running benchmarks, and avoid running the skill with elevated privileges or sensitive environment variables.

Risk: The build script can clone or pull unpinned upstream llama.cpp code and compile it locally.

Mitigation: Review the build directory and git remote before updating, and inspect the upstream revision before compiling.

## Reference(s):

- [llama.cpp](https://github.com/ggerganov/llama.cpp.git)
- [ClawHub skill page](https://clawhub.ai/alexhegit/skills/llamacpp-bench)
- [Publisher profile](https://clawhub.ai/user/alexhegit)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and generated benchmark result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The batch benchmark script writes timestamped Markdown result files under the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
