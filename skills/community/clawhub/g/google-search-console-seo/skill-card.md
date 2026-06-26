## Description: <br>
Google Search Console API integration with managed OAuth for querying search performance analytics, inspecting URL indexing status, reviewing sitemaps, and managing verified site properties. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and SEO operators use this skill to connect an agent to Google Search Console through ClawLink, review verified site data, query search analytics, inspect URL indexing status, and manage sitemaps or site properties. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access to a Google account and Search Console data through ClawLink. <br>
Mitigation: Review the Google account and Search Console permissions during OAuth, and install only when the user intends to connect Google Search Console through ClawLink. <br>
Risk: Write actions such as adding or removing a property or submitting a sitemap can affect Search Console configuration. <br>
Mitigation: Confirm the exact site URL and intended effect with the user before executing any write action. <br>
Risk: Tool calls depend on exact verified Search Console property URLs. <br>
Mitigation: List verified sites first and use the returned site URL exactly, including protocol, subdomain, and trailing slash where applicable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hith3sh/google-search-console-seo) <br>
- [Google Search Console API Overview](https://developers.google.com/webmaster-tools/search-console-api-original) <br>
- [Search Analytics API Reference](https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics) <br>
- [Sites API Reference](https://developers.google.com/webmaster-tools/search-console-api-original/v3/sites) <br>
- [Sitemaps API Reference](https://developers.google.com/webmaster-tools/search-console-api-original/v3/sitemaps) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Google account through ClawLink; write operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
