## Description:

Humanize AI-generated text by detecting and removing patterns typical of LLM output, rewriting text to sound natural and specific, and using pattern detectors, AI vocabulary terms, and statistical analysis to guide edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[actualcwhitlock](https://clawhub.ai/user/actualcwhitlock)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and writing-focused agents use this skill to review drafts for AI-like writing patterns, score text, generate humanization suggestions, and optionally produce revised text that preserves the original meaning and tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic AI-style scores may be misused as decisive evidence in academic, employment, moderation, or other high-stakes decisions.

Mitigation: Use scores as editorial signals only and require human review before making consequential judgments.

Risk: Autofix behavior can change tone, nuance, or quote-sensitive wording.

Mitigation: Keep humanization opt-in for sensitive writing and manually review rewritten output before use.

Risk: Deploying the HTTP API without controls can expose submitted text or invite abuse.

Mitigation: Add authentication, request-size limits, rate limits, privacy and retention notices, and pinned deployment tooling.

## Reference(s):

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659)
- [AI vocabulary reference](references/ai-vocabulary.md)
- [Pattern reference](references/patterns.md)
- [Humanizer style guide](references/style-guide.md)
- [Pattern documentation](docs/PATTERNS.md)
- [Examples](docs/EXAMPLES.md)
- [Integrations](docs/INTEGRATIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown guidance, with optional JSON reports from CLI and API usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include heuristic AI-likeness scores, grouped findings, statistical indicators, editing suggestions, and optional autofixed text.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and package.json report 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
