## Description:

Detects AI writing patterns, scores AI-tell density, and rewrites text into one of several human voice profiles without external dependencies or network calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aboudjem](https://clawhub.ai/user/aboudjem)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content editors use this skill to audit AI-sounding prose, rewrite text for publication, score AI-tell density, or apply targeted edits to Markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may auto-load project-level humanizer-context.md and apply stale or inappropriate voice guidance.

Mitigation: Review humanizer-context.md before use and remove any outdated samples, banned phrases, or project-specific rules that should not affect the current text.

Risk: In-place edit mode can change Markdown files directly.

Mitigation: Use detect or rewrite mode first for important files, then review the resulting changes before applying or keeping edits.

## Reference(s):

- [Hacker News discussion on AI writing patterns](https://news.ycombinator.com/item?id=46646939)
- [Gone Travelling Productions AI writing giveaways](https://gonetravellingproductions.com/2025/08/20/ai-giveaways-in-writing/)
- [Writewithai dead giveaways article](https://writewithai.substack.com/p/10-dead-giveaways-your-content-screams)
- [Wikipedia signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [AIDetectors spotting AI writing patterns](https://www.aidetectors.io/blog/spotting-ai-writing-patterns)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown reports, rewritten prose, concise change summaries, and in-place Markdown file edits when edit mode is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional 0-100 AI-tell score; optional voice, purpose, aggressiveness, and iteration controls.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
