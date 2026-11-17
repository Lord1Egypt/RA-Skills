## Description:

Track international packages by tracking number across 3100+ carriers via 17TRACK, with optional API-key-backed tracking and a Playwright fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shopmeskills](https://clawhub.ai/user/shopmeskills)

### License/Terms of Use:

MIT

## Use Case:

External users, support teams, and developers use this skill to check shipment status, estimate delivery progress, detect carriers, batch-track packages, and explain logistics status codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm commands can execute package code that changed after review.

Mitigation: Use pinned package versions, a controlled build or lockfile, and review package contents before deployment.

Risk: TRACK17_API_KEY may be exposed if configured with broad local or server access.

Mitigation: Store the key in a managed secret store, scope service accounts narrowly, and expose only the minimum MCP surface needed.

Risk: The no-key fallback depends on Playwright and external 17TRACK page behavior.

Mitigation: Prefer the official 17TRACK API for production workflows and monitor fallback failures separately.

## Reference(s):

- [Logistics Tracking ClawHub Skill](https://clawhub.ai/shopmeskills/skills/logistics-tracking)
- [17TRACK API](https://api.17track.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text describing package status, current location, tracking timeline, carrier detection, and status-code advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use TRACK17_API_KEY for best reliability; no-key operation depends on a Playwright-based fallback.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
