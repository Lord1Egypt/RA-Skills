## Description: <br>
Complete methodology for optimizing local llama.cpp and llama-server parameters through controlled performance and quality testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoperealize](https://clawhub.ai/user/hoperealize) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to benchmark local LLM deployments, tune llama.cpp launch parameters, and produce model-specific recommendations for speed, context length, quality, and stability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied llama-server commands could expose a local service if host binding or production networking is changed without review. <br>
Mitigation: Review commands before use, keep local testing bound to 127.0.0.1, and use a reverse proxy with HTTPS for any production exposure. <br>
Risk: Aggressive context, batch, or cache settings can cause OOM failures or unstable local inference. <br>
Mitigation: Tune parameters incrementally, monitor VRAM, and reduce ctx-size or batch-size when crashes occur. <br>
Risk: Systemd service and OpenClaw snippets may not match the user's machine, model path, or context settings. <br>
Mitigation: Treat service and OpenClaw snippets as optional examples and adapt paths, ctx-size, contextWindow, and maxTokens to the local deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoperealize/llama-params-optimizer) <br>
- [llama.cpp official repository](https://github.com/ggerganov/llama.cpp) <br>
- [Qwen3.5 MoE tuning example](example-qwen3.5-moe-4060ti.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, checklists, bash commands, systemd snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local tuning recommendations and example commands that should be reviewed and adapted before use.] <br>

## Skill Version(s): <br>
3.1.0 (source: release evidence, SKILL.md frontmatter, CHANGELOG, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
