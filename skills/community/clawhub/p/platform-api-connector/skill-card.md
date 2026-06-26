## Description: <br>
Connect to social media and content platform APIs by navigating developer portals, creating apps, obtaining OAuth tokens, and storing credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandonwadepackard-cell](https://clawhub.ai/user/brandonwadepackard-cell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to set up and troubleshoot OAuth credentials for Facebook, Instagram, YouTube, Twitter/X, and TikTok integrations. It helps users create platform apps, choose scopes, exchange or refresh tokens, and store credentials in a structured database format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expose API keys, OAuth tokens, client secrets, or refresh tokens while following setup and debugging steps. <br>
Mitigation: Use a secrets vault or encrypted database fields, restrict database access, avoid logging or pasting full tokens, and rotate or revoke credentials when exposure is suspected. <br>
Risk: Overbroad OAuth scopes or write/posting permissions can allow unnecessary account actions. <br>
Mitigation: Request the narrowest scopes possible and add write or posting permissions only when the integration explicitly requires them. <br>
Risk: Platform-specific token lifetimes, app review requirements, and tier limits can cause failed posting or authorization flows. <br>
Mitigation: Confirm current platform requirements, refresh-token behavior, quota limits, and app review status before relying on automated posting. <br>


## Reference(s): <br>
- [OAuth Flow Patterns](references/oauth-flows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code, shell commands] <br>
**Output Format:** [Markdown with JSON, SQL, Python, and HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Credential-handling guidance should be adapted to the user's target platform, approved scopes, and storage system.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
