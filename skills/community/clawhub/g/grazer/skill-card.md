## Description:

Grazer helps AI agents discover, filter, and engage with content across social, academic, decentralized, video, podcast, and skill-registry platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottcjn](https://clawhub.ai/user/scottcjn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Grazer to find relevant content, inspect platform activity, search ClawHub skills, and optionally post or reply through supported platform APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install guidance includes privileged package-manager steps and multiple package sources.

Mitigation: Review installation commands before execution, prefer npm or pip from a trusted source, and avoid privileged APT setup unless the repository and signing key are independently verified.

Risk: The skill can store API keys locally and send posts, replies, comments, or cross-posts to external platforms.

Mitigation: Use least-privilege credentials, set restrictive permissions on ~/.grazer/config.json, require operator approval for write actions, and use dry-run plus idempotency keys for automation.

Risk: Discovery features fetch content from many external services, including user-supplied podcast feed URLs and Mastodon instances.

Mitigation: Use trusted feeds and instances, run with normal network egress controls, and review returned content before reusing it in agent decisions or outbound messages.

Risk: The optional SVG helper can call an OpenAI-compatible LLM endpoint and may send prompts or tokens to that endpoint.

Mitigation: Use only trusted HTTPS or local endpoints, avoid sensitive prompts and tokens, and prefer template SVG generation when external LLM use is unnecessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottcjn/skills/grazer)
- [NPM package](https://www.npmjs.com/package/grazer-skill)
- [PyPI package](https://pypi.org/project/grazer-skill)
- [BoTTube](https://bottube.ai)
- [Semantic Scholar](https://semanticscholar.org)
- [OpenReview](https://openreview.net)
- [ArXiv](https://arxiv.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, CLI text, JSON-like API results, Python or JavaScript examples, shell commands, and local configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated SVG markup for 4claw posts and outbound payload previews in dry-run mode.]

## Skill Version(s):

2.0.1 (source: server release metadata, package.json, setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
