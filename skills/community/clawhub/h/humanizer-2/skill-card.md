## Description: <br>
Humanize AI-generated text by detecting and removing common LLM writing patterns, scoring text for AI-like signals, and suggesting rewrites that preserve meaning while sounding more natural. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ActualCWhitlock](https://clawhub.ai/user/ActualCWhitlock) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Writers, editors, and developers use this skill to review drafts for AI-like wording, get scored analysis, and produce more natural revisions or editing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite drafts to sound less AI-like, which may change tone, claims, or implied authorship. <br>
Mitigation: Review suggested edits before use and avoid changes that invent personal experience, evidence, or authorship claims. <br>
Risk: Drafts may contain confidential, regulated, contractual, or credential-like content. <br>
Mitigation: Prefer local CLI or MCP use for sensitive text, and only send content to a deployed API instance when the operator and retention practices are trusted. <br>
Risk: Always-on style rewriting may be inappropriate for workflows that require a stable voice or unmodified source wording. <br>
Mitigation: Enable always-on mode only where persistent style rewriting is intended and keep human review in the editing loop. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ActualCWhitlock/humanizer-2) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659) <br>
- [blader/humanizer](https://github.com/blader/humanizer) <br>
- [OpenClaw](https://github.com/nichochar/openclaw) <br>
- [AI Vocabulary Reference](references/ai-vocabulary.md) <br>
- [Pattern Reference](references/patterns.md) <br>
- [Style Guide Reference](references/style-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON reports, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scores, pattern findings, rewrite suggestions, auto-fixed text, or integration instructions.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact metadata reports 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
