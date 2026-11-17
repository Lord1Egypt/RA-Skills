## Description:

Rewrite AI-looking drafts in the user's voice, using local samples when available, audience/cognition analysis when useful, then check factual claims against evidence before finalizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fendouai](https://clawhub.ai/user/fendouai)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, marketers, developers, and other external users can use this skill to turn rough or AI-looking drafts into clearer, more specific, better-voiced text. It is most useful when the agent can use user-approved writing samples, audience notes, and evidence sources to preserve voice and check factual claims before final output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use web search for fact checking based on draft-derived claims, which can expose sensitive draft content outside a local workflow.

Mitigation: Use a local-only workflow for confidential drafts or explicitly instruct the agent not to use web search.

Risk: The published package includes prior agent session logs in .omx files.

Mitigation: Remove packaged .omx session files before broad release or enterprise deployment.

Risk: The detector-evasion appendix and external-search consent language could be misunderstood as default behavior.

Mitigation: Review and tighten that documentation so the default workflow remains quality-focused and consent-aware.

## Reference(s):

- [Humanize Skill on ClawHub](https://clawhub.ai/fendouai/skills/humanize-skill)
- [Lynote.ai](https://lynote.ai)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [blader/humanizer](https://github.com/blader/humanizer)
- [Anti-AI patterns: a diagnostic catalog](docs/anti-ai-patterns.md)
- [Audience, cognition, and author persona](docs/audience-persona.md)
- [Voice profile: deep matching](docs/voice-profile-deep.md)
- [Specificity and thought visibility](docs/specificity-and-thought.md)
- [Fact-check: a depth pass for claims](docs/fact-check.md)
- [Detection-aware methods: an alternative methodology](docs/detection-aware-methods.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text rewrites with optional concise editing notes and claim-status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent may use user-selected samples, local exports, and evidence sources when authorized; for confidential drafts, users should keep the workflow local or explicitly disable web search.]

## Skill Version(s):

1.0.2 (source: server release metadata, created 2026-07-24T14:17:32Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
