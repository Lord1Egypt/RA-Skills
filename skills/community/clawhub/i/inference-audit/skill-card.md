## Description:

Compare your AI inference costs across providers and test cheaper alternatives with real data. Analyze what you spend on LLM, embeddings, image generation, TTS, transcription, OCR, video, and reranking, then benchmark a unified API with 30 services and $1 free trial credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fjnunezp75](https://clawhub.ai/user/fjnunezp75)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inventory AI inference providers, compare monthly spend against GPU-Bridge pricing, and benchmark alternative services before deciding whether to migrate or consolidate API usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send prompts, documents, audio, source code, customer data, or regulated data to GPU-Bridge during benchmarking.

Mitigation: Use synthetic or approved test data unless the data disclosure has been reviewed and the provider's privacy and retention terms are acceptable.

Risk: The skill frames recommendations around GPU-Bridge pricing and may produce vendor-specific conclusions.

Mitigation: Treat results as one vendor comparison and review recommendations against current requirements, quality needs, reliability needs, and alternative providers before migration.

## Reference(s):

- [GPU-Bridge API Docs](https://gpubridge.io)
- [GPU-Bridge Service Catalog](https://api.gpubridge.io/catalog)
- [GPU-Bridge Cost Estimator](https://api.gpubridge.io/catalog/estimate?service=llm-4090)
- [ClawHub Skill Page](https://clawhub.ai/fjnunezp75/skills/inference-audit)
- [Publisher Profile](https://clawhub.ai/user/fjnunezp75)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with comparison tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cost estimates, benchmark observations, and migration recommendations based on user-provided provider usage.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
