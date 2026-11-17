## Description:

Browse county property records with GISDB, help users choose search criteria, and save or resume their searches. Review available offers and manage purchases or lead subscriptions only when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mooshee](https://clawhub.ai/user/mooshee)

### License/Terms of Use:

MIT-0

## Use Case:

Property researchers and real estate professionals use the skill to review county property records, understand source coverage and missing information, and save searches. When requested, it also helps users review GISDB offers and manage purchases or lead subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: County records and lead data can be incomplete or out of date, and repeated owner-name labels do not establish identity, ownership, or intent.

Mitigation: Show source dates, coverage, recorded facts, and missing information; keep unsupported conclusions unknown.

Risk: Recurring plans may keep billing when lead updates are paused, and protected order or download links can expose private account information.

Mitigation: Review the exact offer and billing terms before checkout, use cancellation when the user requests stopping renewal, and keep protected links private.

## Reference(s):

- [GISDB setup guide](https://gisdb.io/integrations/0.4.1)
- [GISDB](https://gisdb.io)
- [Research and package selection](artifact/references/research-and-packages.md)
- [Commerce and recovery](artifact/references/commerce-and-recovery.md)
- [Untax integration guide](https://untax.io/integrations/0.4.1#quick-start)
- [Moosh Works](https://mooshworks.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research results reflect available county sources and may include source dates, coverage, and missing information. Purchase, subscription, and delivery status is reported from returned account and order information.]

## Skill Version(s):

0.4.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
