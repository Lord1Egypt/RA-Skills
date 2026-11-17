## Description:

OpenViking Light is a lightweight RAG knowledge base for AI agents that combines local BM25 full-text retrieval with MiniMax LLM answer generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melonbanjing](https://clawhub.ai/user/melonbanjing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to store lightweight text knowledge, search it locally with BM25, and generate answers from retrieved context through a configured MiniMax-compatible chat endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Knowledge-base entries and user questions can be sent to the configured MiniMax-compatible endpoint during Q&A.

Mitigation: Use only trusted approved HTTPS endpoints, lock MINIMAX_API_HOST to that endpoint, and avoid storing secrets or sensitive private notes unless the endpoint and environment are trusted.

Risk: The skill can auto-install a dependency at runtime if jieba is missing.

Mitigation: Pin and install dependencies before runtime in a controlled environment.

## Reference(s):

- [OpenViking Light on ClawHub](https://clawhub.ai/melonbanjing/skills/openviking-light)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from CLI commands, with concise Markdown-style guidance when explaining usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search-only retrieval runs locally; Q&A sends retrieved knowledge and the user question to the configured MiniMax-compatible endpoint.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
