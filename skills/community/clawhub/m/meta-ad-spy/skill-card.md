## Description: <br>
Competitive intelligence skill for researching competitor ads on Meta platforms using the Meta Ad Library, Playwright scraping, and optional Meta Graph API data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhishekj9621](https://clawhub.ai/user/abhishekj9621) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, growth teams, and developers use this skill to collect public Meta Ad Library data, optionally enrich it with Graph API or third-party API results, and synthesize competitor ad intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-based scraping and API calls may send research targets, access tokens, or competitor queries to Meta or optional third-party services. <br>
Mitigation: Use least-privilege, short-lived API keys; confirm targets before third-party requests; run the workflow in a virtual environment or container; and review generated /tmp scripts before execution. <br>
Risk: Raw ad outputs can contain campaign data, creative links, and intermediate research files that users may not want retained. <br>
Mitigation: Clean up temporary scripts and JSON outputs after use, and limit report sharing to intended audiences. <br>


## Reference(s): <br>
- [Meta Ad Spy ClawHub Page](https://clawhub.ai/abhishekj9621/meta-ad-spy) <br>
- [Meta Ad Library](https://www.facebook.com/ads/library/) <br>
- [Meta for Developers](https://developers.facebook.com/) <br>
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/) <br>
- [Meta Ad Library API Field Reference](references/field_reference.md) <br>
- [Page ID Lookup Guide](references/page_id_lookup.md) <br>
- [Third-Party Alternatives](references/alternatives.md) <br>
- [SearchAPI.io Meta Ad Library API](https://www.searchapi.io/docs/meta-ad-library-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell and Python code blocks plus JSON examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary Python scripts and raw JSON outputs under /tmp when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
