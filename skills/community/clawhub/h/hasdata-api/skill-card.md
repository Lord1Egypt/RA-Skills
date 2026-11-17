## Description:

HasData helps agents fetch current web data through the hasdata CLI for search, news, shopping, local business, real estate, jobs, page scraping, screenshots, and structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hasdata](https://clawhub.ai/user/hasdata)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to gather current web, marketplace, local-business, real-estate, job, and page-scraping data through HasData CLI commands. It is suited for grounding answers, checking current facts, enriching public data, summarizing pages, and producing structured JSON or markdown from web sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a third-party CLI through a curl-to-shell command can create supply-chain exposure.

Mitigation: Inspect and verify the installer and CLI source before installation; prefer a reviewed package or pinned release when available.

Risk: Queries, requested URLs, scraped pages, and enrichment targets are processed by a third-party scraping service.

Mitigation: Use the skill only for data the user is authorized to send to HasData and avoid sensitive, confidential, or regulated inputs unless an approved data-handling basis exists.

Risk: Session cookies passed through scraping headers can act like account credentials.

Mitigation: Do not provide cookies or authenticated headers unless the user explicitly authorizes that use and understands the account-access implications.

Risk: Public-data enrichment can produce uncertain or single-source identity, contact, role, or location claims.

Mitigation: Label guesses and single-source results as unverified and cross-check important data before using it for outreach, employment, housing, or other consequential decisions.

## Reference(s):

- [HasData ClawHub skill page](https://clawhub.ai/hasdata/skills/hasdata-api)
- [HasData publisher profile](https://clawhub.ai/user/hasdata)
- [Search references](references/search.md)
- [Web scraping reference](references/web-scraping.md)
- [Data enrichment](references/enrichment.md)
- [E-commerce reference](references/ecommerce.md)
- [Local-business / maps reference](references/local-business.md)
- [Real-estate reference](references/real-estate.md)
- [Jobs reference](references/jobs.md)
- [All commands](references/all-commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; HasData CLI calls return JSON and can produce markdown, text, HTML, screenshots, and structured extraction results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the hasdata binary and a configured HasData API key; CLI responses are commonly piped through jq for extraction.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
