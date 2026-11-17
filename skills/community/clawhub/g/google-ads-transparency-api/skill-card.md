## Description:

Resolve a brand or domain to a Google advertiser id, pull its active ads across Google surfaces, and open a creative with region and impression history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, marketers, and ad-intelligence agents use this skill to resolve Google advertiser identities, inspect live ad creatives, and summarize public transparency data for competitor, political, or campaign research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertiser and domain lookup queries are sent to Scavio, and SCAVIO_API_KEY use may consume account credits.

Mitigation: Install only when that data sharing and credit use are acceptable; budget paginated searches before running them.

Risk: SDK installation or examples could run in an environment with broader privileges or unrelated secrets.

Mitigation: Prefer the direct HTTPS examples or install SDKs in an isolated, non-privileged environment, and expose only SCAVIO_API_KEY.

Risk: Incorrect request limits or geographic assumptions can produce misleading advertising conclusions.

Mitigation: Keep search limits at or below 100, treat non-EEA impression nulls as unpublished data rather than zero, and report Google-provided ranges as ranges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/google-ads-transparency-api)
- [Scavio Google Ads Advertisers documentation](https://scavio.dev/docs/google-ads-advertisers?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ads-transparency-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-ads-transparency-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API response descriptions and Python, JavaScript, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; API responses are structured JSON; each documented endpoint costs one credit.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
