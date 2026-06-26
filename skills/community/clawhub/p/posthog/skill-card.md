## Description: <br>
Interact with PostHog analytics through its REST API to capture events, evaluate feature flags, run HogQL queries, and manage analytics resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonfunk](https://clawhub.ai/user/simonfunk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analytics operators use this skill to work with PostHog projects from an agent, including event capture, feature flag evaluation, HogQL queries, and CRUD-style management of analytics resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to PostHog analytics data and production-affecting changes. <br>
Mitigation: Use least-privilege API keys, avoid admin or write scopes unless required, and manually confirm create, update, delete, and broad HogQL query operations. <br>
Risk: PostHog API keys and project credentials could be exposed through chat transcripts, logs, or command output. <br>
Mitigation: Keep secrets in environment variables, avoid pasting credentials into prompts, and review command output before sharing it. <br>
Risk: Person-level analytics data and session recordings may contain sensitive user information. <br>
Mitigation: Limit access to users with a business need, minimize returned fields and query ranges, and handle exported results as sensitive data. <br>


## Reference(s): <br>
- [PostHog API Endpoint Reference](references/api-endpoints.md) <br>
- [PostHog User API Keys](https://us.posthog.com/settings/user-api-keys) <br>
- [PostHog Project Variables](https://us.posthog.com/settings/project#variables) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PostHog API credentials and project identifiers supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
