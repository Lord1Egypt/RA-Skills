## Description:

Search the web and X (Twitter) using SkillBoss API Hub with real-time access, citations, and image understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to retrieve current web results and X/Twitter discussion for questions requiring up-to-date sources, domain or handle filters, and optional media understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill sends API keys and queries to a different undocumented host.

Mitigation: Use only if that endpoint is authorized for the deployment, avoid sensitive or regulated query content, and rotate the configured API key if the skill was already used without review.

Risk: The security summary says some promised search controls are not enforced.

Mitigation: Treat domain, handle, date, and media controls as best-effort until reviewed, and manually check returned sources before relying on filtered results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-llm)
- [Skill homepage](https://github.com/yourusername/xai-grok-search)
- [SkillBoss API Hub pilot endpoint](https://api.skillbossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Search result text with citations and optional JSON-like metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; search queries may take 30-60+ seconds.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
