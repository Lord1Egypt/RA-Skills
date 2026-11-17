## Description:

Web reading layer for AI agents. Convert any public URL into structured intelligence - entities, business intent, confidence score - in one API call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sid890-cpu](https://clawhub.ai/user/sid890-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to send public web pages to Project Ghost and receive structured page intelligence such as business intent, named entities, confidence scores, token savings, and priority scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested public URLs and resulting page-processing data are sent to Project Ghost's hosted API.

Mitigation: Use only public, non-sensitive URLs unless the provider's terms and data handling practices have been reviewed.

Risk: Authenticated pages, private intranet pages, URLs containing secrets, and sensitive legal or business material could expose confidential information.

Mitigation: Do not submit private or sensitive URLs, authenticated content, URL tokens, or confidential material through the skill.

Risk: Protected or blocked websites may return a blocked-page message instead of extracted intelligence.

Mitigation: Treat blocked responses as no result and verify important findings against the original source before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sid890-cpu/skills/project-ghost)
- [Project Ghost Homepage](https://project-ghost-lilac.vercel.app)
- [Project Ghost API Docs](https://project-ghost-production.up.railway.app)
- [Project Ghost Integration Guide](https://project-ghost-lilac.vercel.app/integrate.html)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Guidance]

**Output Format:** [Markdown guidance with curl commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GHOST_API_KEY and sends requested public URLs to the hosted Project Ghost API.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
