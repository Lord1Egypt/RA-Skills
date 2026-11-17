## Description:

Russian-language travel assistant skill for visa guidance, travel news, RSS feeds, holidays, and currency information using public Letundra.com pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leninws](https://clawhub.ai/user/leninws)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-focused agents use this skill to answer Russian-language questions about visa requirements, travel and aviation news, country holidays, RSS feeds, and currency rates from Letundra.com. It is not intended for booking travel or hotels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public travel information that may be unavailable, stale, incomplete, or unsuitable as the sole basis for travel decisions.

Mitigation: Treat responses as informational and verify visa, holiday, currency, and travel-change details against official or current sources before acting.

Risk: The artifact includes maintainer publishing tooling that uses an authenticated ClawHub CLI session.

Mitigation: Do not run publish-all.sh unless intentionally publishing these skills from an authenticated maintainer environment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/leninws/skills/letundra)
- [Letundra.com](https://letundra.com)
- [Letundra country pages](https://letundra.com/ru/countries/{slug}/)
- [Letundra news](https://letundra.com/ru/news/)
- [Letundra news by tag](https://letundra.com/ru/news/?taglist={tag})
- [Letundra public news feed](https://letundra.com/?yandex_feed=news)

## Skill Output:

**Output Type(s):** [text, markdown, XML, guidance]

**Output Format:** [Markdown and XML snippets with links to source pages where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires access to public Letundra.com pages; the artifact metadata lists node as a required binary for bundled scripts.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
