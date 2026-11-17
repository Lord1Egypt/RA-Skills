## Description:

Meme Lord helps agents explain, create, continue, and combine Chinese internet memes, using web search for meme origins and trend checks when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dox012](https://clawhub.ai/user/dox012)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent decode Chinese internet memes, generate meme-style phrasing, continue meme chains, combine meme formats, and summarize trending meme topics with confidence labels and references when search is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries for meme origins or trends may disclose user-provided text to external search providers.

Mitigation: Avoid sending private, confidential, or sensitive text for lookup; review or redact search terms before using web search.

Risk: Meme origins, meanings, and trend status can be inaccurate, stale, or based on incomplete search results.

Mitigation: Use the skill's confidence labels and source references, and verify important claims with current sources before relying on them.

Risk: Meme generation or continuation can drift into discriminatory, political, abusive, or minor-inappropriate content.

Mitigation: Apply the skill's documented boundaries and decline or redirect requests involving protected-class attacks, political sensitivity, malicious targeting, or inappropriate minor-related content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dox012/skills/meme-lord)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text responses with meme explanations, examples, confidence labels, and source references when search is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external-source links, confidence labels, and freshness labels for meme trend checks.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
