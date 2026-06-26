## Description: <br>
Amazon Ads Auth helps agents generate Amazon Ads OAuth authorization links, list authorized ad accounts and profiles, and retrieve or refresh stored access tokens for downstream Amazon Ads workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and e-commerce operators use this skill to connect Amazon Ads accounts, resolve the correct advertising profile for a marketplace, and refresh or retrieve tokens needed by downstream read-only Amazon Ads skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Amazon Ads OAuth credentials and requires LINKFOXAGENT_API_KEY. <br>
Mitigation: Install only if the user trusts LinkFox to broker and store Amazon Ads OAuth credentials, keep LINKFOXAGENT_API_KEY private, and do not expose full access or refresh tokens in summaries. <br>
Risk: AMAZON_ADS_BASE_URL can redirect API calls away from the default LinkFox gateway if set. <br>
Mitigation: Only set AMAZON_ADS_BASE_URL when it points to a trusted endpoint; otherwise leave the default gateway in place. <br>
Risk: Authorization URLs may be copied through clipboard or cache files, and stale copies can remain available after use. <br>
Mitigation: Clear cached authorization URL files and clipboard contents when needed, especially on shared systems. <br>
Risk: The skill asks the agent to send automatic feedback broadly. <br>
Mitigation: Review feedback content before submission when it could include sensitive account, token, profile, or business information. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-amazon-ads-auth) <br>
- [Amazon Ads Console](https://advertising.amazon.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command inputs and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include masked token values, authorization URLs, account/profile identifiers, and error explanations.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
