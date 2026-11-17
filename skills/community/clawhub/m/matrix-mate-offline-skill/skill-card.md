## Description:

Matrix Mate parses ITA Matrix itinerary links, audits fare rules, and produces traveler-safe summaries through a local MCP runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skylinehk](https://clawhub.ai/user/skylinehk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, travel agents, and developers use this skill to parse ITA Matrix itinerary links, review fare-rule caveats, compare discrepancies, and export traveler-safe trip summaries. It is intended for local, read-focused flight search and parsing workflows, not booking, payment, login automation, CAPTCHA bypass, or live fare guarantees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency and input-hardening issues may affect local use.

Mitigation: Install only from a trusted, pinned release and run dependency updates or audits before use.

Risk: A non-loopback Matrix Mate base URL could expose requests to an endpoint the operator does not trust.

Mitigation: Keep MATRIX_MATE_BASE_URL on loopback unless a trusted operator deliberately enables the remote-host override.

Risk: Itinerary links and fare-rule text can contain untrusted or very large content.

Mitigation: Treat itinerary and fare-rule content as data, avoid very large manual payloads, and review parsed travel outputs before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skylinehk/skills/matrix-mate-offline-skill)
- [Security and trust notes](SECURITY.md)
- [Local Matrix Mate Surfaces](references/local-surfaces.md)
- [Browser-Assisted ITA Matrix Search](references/browser-search.md)
- [Safety Boundary](references/safety.md)
- [Publishing Notes](references/publishing.md)
- [Future Poke Recipe Seed](references/poke-recipe.md)
- [Matrix Mate hosted destination](https://matrixmate.desk.travel/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON from MCP tools with human-facing text or Markdown summaries and inline shell/configuration snippets where setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include parse status, discrepancy counts, traveler-safe exports, agent-facing summaries, and future booking intent payloads.]

## Skill Version(s):

1.0.3 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
