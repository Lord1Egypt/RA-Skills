## Description: <br>
MLX-powered local AI guidance for running LLMs, image generation, speech-to-text, and embeddings on Apple Silicon through an Ollama Herd fleet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and run local Apple Silicon MLX workflows for text generation, image generation, transcription, embeddings, fleet status checks, and hardware-aware model recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup and operation may install local tools, start local services, and interact with a live model fleet. <br>
Mitigation: Run the commands only in a trusted macOS development environment and review package installation, service startup, and API calls before execution. <br>
Risk: Model management can consume local storage or alter available models. <br>
Mitigation: Require explicit confirmation for model pulls and deletions, and avoid deleting or modifying files under ~/.fleet-manager. <br>
Risk: The server security review describes the package as clean but still recommends trusting the maintainer workflow before installation. <br>
Mitigation: Install only when the publisher and release are trusted, and re-scan or review the skill before deployment in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/mlx-apple-silicon-mlx) <br>
- [MLX framework](https://github.com/ml-explore/mlx) <br>
- [Ollama Herd](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash, Python, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference macOS-only requirements, local service endpoints, and optional Python tooling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
