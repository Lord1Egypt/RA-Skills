## Description:

Hot Search is an OpenClaw search skill for financial data and market information that aggregates Bing CN, Bing Global, Yandex, and Swisscows results without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fishsome](https://clawhub.ai/user/fishsome)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve search result titles, links, and snippets for market, financial, news, and general web queries across multiple public search engines. The artifact also exposes Bing image search and image download helpers, which should be restricted before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are disclosed to third-party search engines.

Mitigation: Avoid sensitive trading, client, proprietary, or regulated queries and review retrieved results before relying on them.

Risk: Image download helpers can fetch arbitrary URLs and write local files.

Mitigation: Expose image downloading only with HTTPS-only public hosts, validated image content, size limits, and a fixed non-overwriting download directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fishsome/skills/hot-search)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [JSON-like result dictionaries and command-line text containing titles, links, snippets, engine names, and optional downloaded image paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search behavior depends on third-party search engine availability, HTML structure, timeout settings, and configured request delay.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
