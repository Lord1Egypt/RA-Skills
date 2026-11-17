## Description:

Find podcasts suited to a proposed guest using Crawlora's podcast catalog, live show and episode data, and public show websites for sourced shortlists and tailored pitch angles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast booking teams, publicists, and prospective guests use this skill to research relevant shows, check recent episodes and public submission channels, and draft evidence-backed guest pitch angles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends the Crawlora API key and research requests to Crawlora.

Mitigation: Use the documented research endpoints and keep CRAWLORA_API_KEY out of logs, commits, and shared transcripts.

Risk: Podcast metadata and chart rankings may be stale or mistaken for audience size or booking availability.

Mitigation: Check live episode dates and public show sites; label coverage gaps, audience size, and booking availability as unknown unless independently verified.

## Reference(s):

- [Podcast research endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/podcast-guest-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown shortlist with sourced show and episode details, pitch angles, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes links, episode dates, verified submission channels when available, and explicit unknowns; does not send pitches without a request.]

## Skill Version(s):

1.0.13 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
