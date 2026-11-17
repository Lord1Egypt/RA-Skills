## Description:

Routes LLM requests to a local model such as Ollama, LM Studio, or llamafile before falling back to cloud APIs, while tracking token savings and cost avoidance in a persistent dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelnishanth](https://clawhub.ai/user/joelnishanth)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to prefer local LLM execution for lower-cost or more private requests, decide when to fall back to cloud models, and review cumulative routing savings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider setup can involve running downloaded installer or binary code that has not been verified.

Mitigation: Install local providers only through verified package-manager flows or pinned checksum/signature procedures.

Risk: Cloud fallback can send prompt content outside the local environment when no local provider is available or when complexity routing selects cloud.

Mitigation: Treat each cloud routing decision as explicit approval to send the prompt externally, especially for private or regulated data.

Risk: Savings history is written to a persistent file in the user's home directory.

Mitigation: Avoid logging sensitive request details and reset or remove the savings file when local records should not be retained.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joelnishanth/skills/local-first-llm)
- [Routing Decision Logic](artifact/references/routing-logic.md)
- [Local LLM Provider Setup](artifact/references/local-providers.md)
- [Token Estimation and Cloud Cost Reference](artifact/references/token-estimation.md)
- [LM Studio](https://lmstudio.ai)
- [llamafile Releases](https://github.com/Mozilla-Ocho/llamafile/releases)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON outputs from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists savings data at ~/.openclaw/local-first-llm/savings.json and checks localhost providers for Ollama, LM Studio, and llamafile.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
