## Description: <br>
Access Google Search Console API via cURL with OAuth to manage sites, sitemaps, and query search analytics including clicks, impressions, and rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otman-ai](https://clawhub.ai/user/otman-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to call Google Search Console through Maton-managed OAuth, inspect site performance, query search analytics, and manage sitemap entries from cURL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and OAuth connection details can be exposed if pasted into shared terminals, logs, or screenshots. <br>
Mitigation: Use a private Maton API key, keep it in an environment variable, and avoid echoing or sharing secret values. <br>
Risk: PUT and DELETE examples can change sitemap configuration or remove an OAuth connection. <br>
Mitigation: Replace sample IDs with verified connection and site values, then review administrative commands before running them. <br>
Risk: Requests are routed through Maton as a gateway to Google Search Console. <br>
Mitigation: Install and use this skill only when Maton is the intended gateway for Google Search Console access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/otman-ai/google-search-console-maton) <br>
- [Maton](https://maton.ai) <br>
- [Maton Settings](https://maton.ai/settings) <br>
- [Maton Connection Management](https://ctrl.maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with cURL commands, JSON request examples, and endpoint notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Maton API key and OAuth connection identifiers supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
