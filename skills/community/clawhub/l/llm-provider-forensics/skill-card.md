## Description: <br>
Forensically verify what model family or routing layer may actually sit behind a claimed LLM endpoint or model ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate whether a claimed LLM provider endpoint is genuine, routed, wrapped, aggregated, or unusable. It supports confidence-based operational decisions about provider selection, fallback, or avoidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses configured provider API keys and sends test prompts to external LLM services, which may consume quota or create provider-side logs. <br>
Mitigation: Before running, verify the config path, selected provider names, model ID, and whether the deep probe suite is needed. <br>
Risk: Family and routing conclusions are confidence-based, and protocol compatibility alone does not prove the underlying model family. <br>
Mitigation: Use the final judgment and need-human-review sections to separate protocol-layer evidence from suspected model-family evidence before making operational decisions. <br>


## Reference(s): <br>
- [LLM Provider Forensics release](https://clawhub.ai/andyrenxu7255/llm-provider-forensics) <br>
- [Forensics Checklist](references/forensics-checklist.md) <br>
- [Advanced Forensics Dimensions](references/advanced-dimensions.md) <br>
- [Streaming / Error / Variance Heuristics](references/error-stream-variance.md) <br>
- [OpenAI-Compatible Protocol Rules](references/protocol-openai.md) <br>
- [Anthropic-Compatible Protocol Rules](references/protocol-anthropic.md) <br>
- [Gemini-Compatible Protocol Rules](references/protocol-gemini.md) <br>
- [GLM / Zhipu Protocol Rules](references/protocol-glm.md) <br>
- [GPT / OpenAI Family Fingerprint](references/fingerprint-gpt.md) <br>
- [Claude / Anthropic Family Fingerprint](references/fingerprint-claude.md) <br>
- [Gemini / Google Family Fingerprint](references/fingerprint-gemini.md) <br>
- [GLM / Zhipu Family Fingerprint](references/fingerprint-glm.md) <br>
- [Kimi / Moonshot Family Fingerprint](references/fingerprint-kimi.md) <br>
- [MiniMax Family Fingerprint](references/fingerprint-minimax.md) <br>
- [DeepSeek Family Fingerprint](references/fingerprint-deepseek.md) <br>
- [Claude Native Deep Tests](references/deep-claude.md) <br>
- [Gemini Native Deep Tests](references/deep-gemini.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report sections or JSON probe output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are confidence-based and include protocol findings, suspected model-family findings, stability results, capability findings, review items, and operational posture.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
