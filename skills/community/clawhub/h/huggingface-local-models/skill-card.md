## Description:

Use to select models to run locally with llama.cpp and GGUF on CPU, Mac Metal, CUDA, or ROCm. Covers finding GGUFs, quant selection, running servers, exact GGUF file lookup, conversion, and OpenAI-compatible local serving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huggingface](https://clawhub.ai/user/huggingface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find Hugging Face GGUF models, choose suitable quantization, construct llama.cpp commands, and run local OpenAI-compatible model servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to install or build llama.cpp before running local models.

Mitigation: Review generated install and build commands before execution and use trusted llama.cpp distribution sources.

Risk: The skill may guide an agent to authenticate to Hugging Face and download large or gated model files.

Mitigation: Authenticate only when needed, use trusted model repositories, and check model licenses before download or use.

Risk: The skill may guide an agent to start a local llama-server endpoint.

Mitigation: Bind local servers appropriately for the environment and restrict access to OpenAI-compatible endpoints during testing.

## Reference(s):

- [Hub discovery workflow](references/hub-discovery.md)
- [GGUF quantization guide](references/quantization.md)
- [Hardware acceleration](references/hardware.md)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [Hugging Face GGUF and llama.cpp docs](https://huggingface.co/docs/hub/gguf-llamacpp)
- [Hugging Face Local Apps docs](https://huggingface.co/docs/hub/main/local-apps)
- [Hugging Face Local Agents docs](https://huggingface.co/docs/hub/agents-local)
- [GGUF converter Space](https://huggingface.co/spaces/ggml-org/gguf-my-repo)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, text, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include URLs, exact GGUF filenames, quantization recommendations, and local server smoke-test requests.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
