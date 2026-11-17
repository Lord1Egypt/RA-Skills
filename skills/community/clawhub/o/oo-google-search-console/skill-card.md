## Description:

Use an OOMOL-connected Google Search Console account to inspect properties, search performance, URLs, and sitemaps, and to manage sites and sitemaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to retrieve Search Console performance and indexing information, inspect sites and URLs, and manage sites or sitemaps through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can run downloaded code that may change between releases without separate approval or integrity checks.

Mitigation: Use a reviewed, version-pinned CLI installation and control automatic skill synchronization.

Risk: Search Console actions can modify or delete account data.

Mitigation: Review the Google account permissions granted through OOMOL and retain the skill's confirmation requirements for write and destructive actions.

## Reference(s):

- [Google Search Console](https://search.google.com/search-console)
- [Google Search Console API reference](https://developers.google.com/webmaster-tools/v1/api_reference_index)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-google-search-console)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action results and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read and write actions are available; the skill requires confirmation for writes and destructive changes.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
