## Description:

Personal Agent shopping skill for OpenClaw and agentic commerce hosts that converts shopping or gifting intent plus local preference context into SellToAI A2A2A product cards with creator videos, personalization and understanding traces, community evidence, and attribution-tracked buy links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxlie](https://clawhub.ai/user/zxlie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agentic commerce hosts use this skill to turn shopping or gifting requests into SellToAI product recommendations with creator video proof, personalization rationale, and attribution-preserving purchase links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping intent, budget, recipient details, preferences, and memory-derived summaries may be sent to SellToAI or a configured gateway.

Mitigation: Send only compact preference and constraint summaries, avoid raw notes or chat history, and disable memory sharing unless personalization is intended.

Risk: The installer can download remote content and install the skill into several local agent applications.

Mitigation: Prefer manual installation from reviewed artifact files and avoid curl-to-bash installation for sensitive environments.

Risk: Returned purchase links may include commercial attribution or tracking.

Mitigation: Treat buy links as commercially attributed links and preserve them exactly only when the user wants shopping recommendations.

## Reference(s):

- [SellToAI homepage](https://selltoai.ai)
- [ClawHub skill page](https://clawhub.ai/zxlie/skills/mroas-shop)
- [Recommend by intent example](examples/recommend.md)
- [Creator showcase example](examples/creator.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured product-card rendering instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to render returned cards or A2UI JSONL surfaces; returned buy and video URLs must be preserved exactly.]

## Skill Version(s):

0.1.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
