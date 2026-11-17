## Description:

Guidance for building and reviewing Gradio Spaces that use Hugging Face Spaces ZeroGPU, including @spaces.GPU usage, quota and duration tuning, process isolation, concurrency, CUDA dependency constraints, and supported dependency patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huggingface](https://clawhub.ai/user/huggingface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when writing, reviewing, or debugging Gradio SDK Spaces on Hugging Face ZeroGPU hardware. It helps them structure @spaces.GPU handlers, tune duration and size settings, avoid process-boundary serialization errors, handle concurrent requests safely, and choose compatible CUDA dependency installation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct binary wheel URLs can create supply-chain and compatibility risk when installing CUDA-dependent packages.

Mitigation: Prefer official PyPI or verified upstream releases, pin exact versions and immutable URLs, and record or verify SHA-256 hashes for direct binary wheels.

Risk: Concurrent ZeroGPU requests can corrupt shared state or overwrite outputs when code uses mutable globals or fixed output paths.

Mitigation: Keep request data local or in gr.State, treat read-only globals as the safe default, and use unique temporary paths for generated outputs.

Risk: ZeroGPU process isolation can fail or hang when handlers pass unpicklable objects or return CUDA tensors across the worker boundary.

Mitigation: Pass and return picklable values only, move tensors to CPU before returning them, and avoid relying on reference semantics for gr.State.

Risk: Incorrect duration, size, or dependency pins can cause avoidable quota failures, longer queues, or build/import failures.

Mitigation: Set realistic @spaces.GPU duration values, use xlarge only when needed, pin supported Python and torch versions, and match CUDA wheel tags to the Space runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huggingface/skills/huggingface-zerogpu)
- [Hugging Face ZeroGPU documentation](https://huggingface.co/docs/hub/spaces-zerogpu)
- [Hugging Face ZeroGPU AoTI blog](https://huggingface.co/blog/zerogpu-aoti)
- [Hugging Face kernels-community](https://huggingface.co/kernels-community)
- [FlashAttention releases](https://github.com/Dao-AILab/flash-attention/releases)
- [Concurrency Safety](references/concurrency.md)
- [CUDA Dependencies on ZeroGPU](references/cuda-and-deps.md)
- [How Quota Works](references/how-quota-works.md)
- [How ZeroGPU works](references/how-zerogpu-works.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, bash, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend dependency pins, Space README frontmatter settings, @spaces.GPU parameters, and code changes for ZeroGPU compatibility.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
