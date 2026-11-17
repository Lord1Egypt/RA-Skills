## Description:

Fetches web page content through Jina AI's r.jina.ai service, including arbitrary URLs and Google search result pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch public webpage text through Jina AI with curl commands, including search result pages and example public sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs, search terms, and retrieved public page content are sent to Jina AI.

Mitigation: Use the skill only for public, non-sensitive pages and search terms where third-party processing is acceptable.

Risk: URLs can contain secrets or sensitive query parameters.

Mitigation: Do not use private intranet links, authenticated pages, confidential documents, regulated data, or URLs containing tokens, credentials, or sensitive parameters.

Risk: Google result fetching through r.jina.ai may still be blocked when Google access is restricted.

Mitigation: Treat search-result fetching as best effort and verify important retrieved content from an authoritative source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/skills/jina-web-fetcher)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; fetched content is returned as text from r.jina.ai.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sending requested URLs and search terms to Jina AI; no API key or credential variable is indicated by the evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
