## Description: <br>
LinkedIn API integration with managed OAuth for sharing posts, managing profiles and organizations, uploading media, accessing ad and job library data, and using LinkedIn advertising features when the required scopes are granted. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to make LinkedIn API requests through Maton-managed OAuth for profile lookup, organization data, post publishing, media upload, public ad/job library search, and advertising account or campaign workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Maton-managed OAuth and a Maton API key to access LinkedIn on the user's behalf. <br>
Mitigation: Install only when the user trusts Maton, keep MATON_API_KEY protected, and review the OAuth scopes granted to the LinkedIn connection. <br>
Risk: Requests may post public content, delete resources, or change ad accounts and campaigns when the connected account has write or advertising scopes. <br>
Mitigation: Require explicit user confirmation for every create, update, delete, ad account, campaign, budget, or targeting change, including the exact operation and request body or key parameters. <br>
Risk: Multiple LinkedIn connections can route a request to the wrong account if no connection is specified. <br>
Mitigation: Use the Maton-Connection header when more than one LinkedIn connection is available. <br>
Risk: Advertising operations can have financial or compliance impact, especially budget and targeting changes. <br>
Mitigation: Confirm budget amounts, targeting criteria, granted advertising scopes, and compliance with LinkedIn advertising policies before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/linkedin-api) <br>
- [LinkedIn API Overview](https://learn.microsoft.com/en-us/linkedin/) <br>
- [Share on LinkedIn Guide](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin) <br>
- [LinkedIn Profile API](https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/profile-api) <br>
- [LinkedIn Authentication Guide](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication) <br>
- [LinkedIn Marketing API](https://learn.microsoft.com/en-us/linkedin/marketing/) <br>
- [LinkedIn Ad Accounts](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-accounts) <br>
- [LinkedIn Campaign Management](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns) <br>
- [LinkedIn Ad Library API](https://www.linkedin.com/ad-library/api/) <br>
- [Maton Settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with Python, JavaScript, bash, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY, network access, LinkedIn-Version headers, and appropriate LinkedIn OAuth scopes for the requested operation.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
