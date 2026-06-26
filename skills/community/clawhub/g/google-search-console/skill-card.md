## Description: <br>
Google Search Console API integration with managed OAuth for querying search analytics, managing sitemaps, and monitoring site performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to access Google Search Console data through Maton-managed OAuth, including site listings, search analytics, sitemap operations, and connection management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton API keys and OAuth-backed Google Search Console access are sensitive credentials. <br>
Mitigation: Keep MATON_API_KEY private, install only when comfortable granting Maton-managed access, and avoid exposing keys in shared logs or command output. <br>
Risk: Requests can affect the wrong Search Console account when multiple Google connections are active. <br>
Mitigation: Use the Maton-Connection header to select the intended connection before making account-specific requests. <br>
Risk: Sitemap or connection write operations can modify connected Search Console state. <br>
Mitigation: Review the target resource and intended effect with the user before approving create, update, or delete calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/google-search-console) <br>
- [Google Search Console API Reference](https://developers.google.com/webmaster-tools/v1/api_reference_index) <br>
- [Sites: list](https://developers.google.com/webmaster-tools/v1/sites/list) <br>
- [Search Analytics: query](https://developers.google.com/webmaster-tools/v1/searchanalytics/query) <br>
- [Sitemaps](https://developers.google.com/webmaster-tools/v1/sitemaps) <br>
- [Maton API Key Settings](https://maton.ai/settings) <br>
- [Maton Community](https://discord.com/invite/dBfFAcefs2) <br>
- [Maton Support](mailto:support@maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, JavaScript, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and explicit approval before create, update, or delete operations.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
