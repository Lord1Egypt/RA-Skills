## Description:

[Didoo AI] Step-by-step guide for setting up Meta Conversions API (CAPI) server-side event tracking that improves conversion measurement accuracy and reduces CPA discrepancy vs pixel-only tracking, for use when setting up tracking for a new account or when CPA shown in Meta Ads Manager is significantly higher than actual leads/sales.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, developers, and operators use this skill to set up Meta Conversions API tracking, choose an integration method, configure conversion events, and test that Pixel and CAPI events are deduplicated correctly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meta access tokens can expose Business and Marketing API capabilities if mishandled.

Mitigation: Protect the token like a password, store it outside source control, and confirm the token has only the permissions needed for CAPI setup.

Risk: CAPI events can include customer identifiers or conversion data that may be subject to privacy, consent, and regional compliance requirements.

Mitigation: Confirm authorization and consent before sending data to Meta, use HTTPS, and hash supported personal identifiers with SHA-256 before transmission.

Risk: Incorrect Pixel and CAPI deduplication can double-count events or distort campaign measurement.

Mitigation: Pass matching event_id and event_name values for the same conversion and test events in Meta Events Manager before relying on reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elias-didoo/skills/meta-ads-capi-setup)
- [Meta Graph API events endpoint](https://graph.facebook.com/v21.0/{pixel_id}/events)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with setup steps, checklists, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; advises manual CAPI setup, event testing, deduplication checks, and secure token handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
