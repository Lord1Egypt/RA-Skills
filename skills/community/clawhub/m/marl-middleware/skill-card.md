## Description:

Multi-stage multi-agent reasoning middleware that reduces LLM hallucination by 70%+. 9 specialized emergence engines for invention, creative, pharma, genomics, chemistry, ecology, law, recipe, and document generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutechicken99](https://clawhub.ai/user/cutechicken99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route OpenAI-format LLM calls through MARL's multi-stage reasoning middleware for verification, synthesis, and domain-specific reasoning modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to route all configured LLM traffic through MARL and then to the selected backend provider.

Mitigation: Install only when that routing model is acceptable for the deployment and review which backend provider receives the traffic.

Risk: The release uses an opaque, unpinned third-party executable.

Mitigation: Prefer a pinned image digest or exact package version, run with minimal privileges, and avoid unnecessary secrets or mounts.

Risk: The privacy claim may not apply when requests are forwarded to non-local model providers.

Mitigation: Treat the privacy claim as applying only to fully local model deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cutechicken99/skills/marl-middleware)
- [PyPI Package](https://pypi.org/project/marl-middleware/)
- [GitHub Repository](https://github.com/Vidraft/MARL)
- [Hugging Face Demo](https://huggingface.co/spaces/VIDraft/MARL)
- [FINAL Bench Leaderboard](https://huggingface.co/spaces/FINAL-Bench/Leaderboard)
- [VIDRAFT Website](https://vidraft.net)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Text]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides model configuration examples and mode-selection guidance for OpenAI-compatible LLM endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
