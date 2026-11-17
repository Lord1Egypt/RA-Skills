## Description:

Find professional emails and contacts from a name + company/domain using SerpAPI + OpenAI GPT-4o-mini.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrnsmh](https://clawhub.ai/user/mrnsmh)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to find professional contact leads for a company or domain, optionally focused on a named person. It supports prospecting workflows that need candidate emails, LinkedIn URLs, titles, and confidence labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup targets and search snippets may be sent to SerpAPI or Brave and OpenAI.

Mitigation: Use the skill only with a lawful basis for the lookup and avoid sensitive targets unless the data-sharing path is acceptable.

Risk: Returned emails may be guessed or inferred rather than verified.

Mitigation: Treat results as leads, independently confirm addresses before outreach, and rely on confidence labels when triaging.

Risk: API-key fragments or other sensitive operational details may appear in logs.

Mitigation: Scrub logs before sharing, remove key prefixes from operational logging, and rotate credentials if exposure is suspected.

## Reference(s):

- [Email Patterns Reference](references/patterns.md)
- [SerpAPI](https://serpapi.com)
- [SerpAPI Search API](https://serpapi.com/search)
- [Brave Search API](https://api.search.brave.com/res/v1/web/search)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal table by default, with optional JSON contact records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns candidate contacts with email, LinkedIn URL, title, name, confidence, and source when available.]

## Skill Version(s):

0.1.0 (source: server release metadata; skill frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
