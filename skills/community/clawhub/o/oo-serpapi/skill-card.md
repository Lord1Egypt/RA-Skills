## Description:

SerpApi (serpapi.com). Use this skill for ANY SerpApi request — searching and reading data. Whenever a task involves SerpApi, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users with an OOMOL-connected SerpApi account use this skill to run Google web, News, and Maps searches and retrieve search data through SerpApi.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup instructions include a remote CLI installer whose exact effects are unverified.

Mitigation: Review and install a verified CLI release yourself, and require approval before dependency setup or installation of additional agent skills.

Risk: Search queries pass through OOMOL to SerpApi.

Mitigation: Exclude secrets and unnecessary private information from search queries.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [SerpApi](https://serpapi.com)
- [SerpApi Search API documentation](https://serpapi.com/search-api)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Search results and requested data returned as JSON, with summaries or guidance in text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search action schemas determine the available inputs and response fields.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
