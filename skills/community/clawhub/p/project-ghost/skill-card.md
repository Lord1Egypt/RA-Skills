## Description: <br>
Web reading layer for AI agents that converts public URLs into structured intelligence, including entities, business intent, and confidence scores, in one API call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sid890-cpu](https://clawhub.ai/user/Sid890-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Project Ghost to let research, news monitoring, sales, legal, and web-analysis agents summarize public webpages and extract structured signals through a hosted API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested URLs, page contents, and related metadata to the hosted Project Ghost service. <br>
Mitigation: Use it for public webpages only, and avoid sensitive or internal links unless the provider's data handling is acceptable for the use case. <br>
Risk: The skill requires a Project Ghost API key. <br>
Mitigation: Store GHOST_API_KEY in an environment variable or secret manager and avoid exposing it in prompts, command history, logs, or shared files. <br>
Risk: Some protected websites may be blocked or return a blocked-page message instead of structured intelligence. <br>
Mitigation: Handle blocked responses explicitly and verify important findings against the original public source when accuracy matters. <br>


## Reference(s): <br>
- [Project Ghost on ClawHub](https://clawhub.ai/Sid890-cpu/project-ghost) <br>
- [Project Ghost homepage](https://project-ghost-lilac.vercel.app) <br>
- [Project Ghost API docs](https://project-ghost-production.up.railway.app) <br>
- [Project Ghost integration guide](https://project-ghost-lilac.vercel.app/integrate.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown setup guidance with curl examples and a JSON API response shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GHOST_API_KEY and sends requested public URLs, page contents, and related metadata to the hosted Project Ghost service.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
