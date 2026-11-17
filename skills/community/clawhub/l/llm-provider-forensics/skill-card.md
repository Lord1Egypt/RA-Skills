## Description:

Forensically verifies what model family or routing layer may actually sit behind a claimed LLM endpoint or model ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate whether claimed LLM endpoints are genuine, proxied, aliased, aggregated, wrapped, or unusable across common provider protocols and model families.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads selected OpenClaw provider credentials and sends authenticated probes to configurable endpoints, and the server security summary notes insufficient destination safeguards.

Mitigation: Use disposable or least-privileged API keys, verify each base URL before running probes, avoid unknown gateways, and treat deep probes as higher exposure because they send additional test prompts.

Risk: Forensic conclusions are confidence-based and can be misleading if protocol compatibility is treated as proof of model family or publisher identity.

Mitigation: Keep protocol-layer findings separate from suspected model-family findings, preserve uncertainty in the final judgment, and require human review for operational decisions.

## Reference(s):

- [Advanced Forensics Dimensions](references/advanced-dimensions.md)
- [Claude Native Deep Tests](references/deep-claude.md)
- [Gemini Native Deep Tests](references/deep-gemini.md)
- [Streaming / Error / Variance Heuristics](references/error-stream-variance.md)
- [Claude / Anthropic Family Fingerprint](references/fingerprint-claude.md)
- [DeepSeek Family Fingerprint](references/fingerprint-deepseek.md)
- [Gemini / Google Family Fingerprint](references/fingerprint-gemini.md)
- [GLM / Zhipu Family Fingerprint](references/fingerprint-glm.md)
- [GPT / OpenAI Family Fingerprint](references/fingerprint-gpt.md)
- [Kimi / Moonshot Family Fingerprint](references/fingerprint-kimi.md)
- [MiniMax Family Fingerprint](references/fingerprint-minimax.md)
- [LLM Provider Forensics Checklist](references/forensics-checklist.md)
- [Anthropic-Compatible Protocol Rules](references/protocol-anthropic.md)
- [Gemini-Compatible Protocol Rules](references/protocol-gemini.md)
- [GLM / Zhipu Protocol Rules](references/protocol-glm.md)
- [OpenAI-Compatible Protocol Rules](references/protocol-openai.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with ordered findings and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Confidence-based conclusions that separate protocol-layer evidence from suspected model-family evidence.]

## Skill Version(s):

1.3.2 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
