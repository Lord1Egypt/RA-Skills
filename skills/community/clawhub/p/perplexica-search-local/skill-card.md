## Description:

AI-powered search using your local Perplexica instance that runs deep research with web search and LLM reasoning, then returns answers with cited sources in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eplt](https://clawhub.ai/user/eplt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to ask a local Perplexica instance for AI-powered web, academic, or discussion search results with cited answers. It is intended for workflows where search and RAG state remain in Perplexica while the agent receives the answer and sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may leave the user's machine through the local Perplexica instance's configured search and LLM providers.

Mitigation: Install only when running and trusting a local Perplexica instance, and review Perplexica provider configuration before sending sensitive queries.

Risk: Broad or ambiguous prompts can trigger unintended searches.

Mitigation: Use explicit Perplexica wording for sensitive workflows and reserve this skill for requests that clearly need local Perplexica search.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eplt/skills/perplexica-search-local)
- [Perplexica](https://github.com/ItzCrazyKns/Perplexica)
- [OpenClaw](https://open-claw.bot)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown-style answer with cited sources, or raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include query, mode, selected sources, cited source metadata, selected model, and elapsed time.]

## Skill Version(s):

1.0.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
