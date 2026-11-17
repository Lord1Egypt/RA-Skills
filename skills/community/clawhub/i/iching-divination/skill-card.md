## Description:

Iching Divination helps an agent answer I Ching and fortune-telling requests by generating hexagrams and offering Chinese-language interpretations with practical advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaxint](https://clawhub.ai/user/jaxint)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to respond to questions about divination, I Ching hexagrams, fortune, career, business, finance, and relationship decisions. The skill frames outputs as advisory reflection rather than a fixed prediction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User questions may be sent to an undisclosed third-party AI endpoint by default.

Mitigation: Disclose the endpoint and data sent, and make remote AI interpretation opt-in before deployment.

Risk: The artifact includes a hardcoded API key.

Mitigation: Remove the embedded key, rotate the credential, and require runtime secret injection through an environment variable.

Risk: The skill requests broader tool permissions than the feature requires.

Mitigation: Narrow allowed tools and activation scope to explicit divination requests and the minimum required execution path.

Risk: Divination-style guidance could be mistaken for determinative advice for life, business, finance, or relationship decisions.

Mitigation: Keep outputs framed as reflective guidance and remind users to apply independent judgment for consequential choices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaxint/skills/iching-divination)
- [I Ching overview](https://zh.wikipedia.org/wiki/易经)
- [Sixty-four hexagrams reference](https://www.iching.cn/)
- [Ruan Yifeng I Ching introduction](https://www.ruanyifeng.com/blog/blog_iching.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese text with hexagram details, a reading, and practical suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include deterministic hexagram data and optional remote AI interpretation.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
