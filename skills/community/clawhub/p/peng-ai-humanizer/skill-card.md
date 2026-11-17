## Description:

Humanize AI-generated text by detecting common LLM writing patterns, scoring drafts, and suggesting natural rewrites that preserve the original meaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penglovemeng](https://clawhub.ai/user/penglovemeng)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, developers, and writing agents use this skill to review drafts for AI-like phrasing, get pattern-specific guidance, and produce more natural human-facing prose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-detection scores and labels can be mistaken for proof of authorship.

Mitigation: Use the score as editing guidance only, and avoid treating it as an authority in academic, compliance, employment, or authorship decisions.

Risk: Auto-fixed or humanized text can alter meaning, tone, citations, or compliance-sensitive language.

Mitigation: Review generated revisions before use and compare them against the source text for accuracy and intent.

Risk: Always-on prompt templates can persistently change an agent's writing style across unrelated tasks.

Mitigation: Apply always-on guidance only to dedicated writing agents or after explicit user consent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/penglovemeng/skills/peng-ai-humanizer)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Copyleaks stylistic fingerprint research](https://arxiv.org/abs/2503.01659)
- [blader/humanizer](https://github.com/blader/humanizer)
- [Pattern documentation](references/patterns.md)
- [AI vocabulary reference](references/ai-vocabulary.md)
- [Human writing style guide](references/style-guide.md)
- [Examples](docs/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text, Markdown reports, JSON analysis, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scores, matched writing patterns, statistics, prioritized suggestions, and optional auto-fixed text.]

## Skill Version(s):

2.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
