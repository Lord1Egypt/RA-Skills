## Description:

Builds contact-ready KOL and influencer research reports from TikTok, Instagram, or YouTube profile URLs using AIsa WaveInflu email lookup and similar-creator APIs without inventing missing contact data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to research creators, discover similar YouTube or TikTok profiles, retrieve API-sourced creator contact emails, and produce an outreach-ready contact table from a verified seed profile URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send creator profile URLs to AIsa and produce privacy-sensitive creator email data.

Mitigation: Use it only for authorized influencer research, keep generated reports access-controlled, and avoid publishing or transmitting contact lists without separate authorization.

Risk: Incorrect seed URLs or weak hostname validation could enrich the wrong profile or fail unexpectedly.

Mitigation: Verify profile URLs before enrichment and use only TikTok, Instagram, or YouTube creator profile URLs, not individual post or video URLs.

Risk: Bulk enrichment can consume API quota and may enable spam-like outreach workflows.

Mitigation: Confirm scope before more than 25 email lookups, respect quota limits, and do not initiate outreach from the generated list without separate user approval.

## Reference(s):

- [WaveInflu API Reference](references/api-reference.md)
- [KOL Contact & Similar Creator Report Template](references/report-template.md)
- [WaveInflu Email Lookup API](https://aisa.one/docs/api-reference/waveinflu/post_waveinflu-email-lookup)
- [WaveInflu Similar Creators API](https://aisa.one/docs/api-reference/waveinflu/post_waveinflu-similar)
- [AIsa API Reference](https://aisa.one/docs/api-reference)
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/skills/kol-creator-discovery)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional JSON output and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include creator profile URLs, similarity scores, contact-email status, coverage notes, and quota limitations; raw API payloads are not exposed unless requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
