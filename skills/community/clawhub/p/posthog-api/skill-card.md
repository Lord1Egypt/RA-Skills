## Description: <br>
PostHog API integration with managed authentication for product analytics, feature flags, session recordings, experiments, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analytics teams use this skill to query PostHog data through Maton-managed authentication, manage feature flags, inspect user behavior, view session recordings, and run experiments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton proxies requests to the connected PostHog account and requires a sensitive MATON_API_KEY. <br>
Mitigation: Install only if you trust Maton to handle the account data path, and keep MATON_API_KEY private. <br>
Risk: PostHog persons and session recordings can expose emails, identifiers, replay details, and other sensitive analytics data. <br>
Mitigation: Minimize retrieval of persons and session recordings, and avoid exposing raw emails or replay details unless necessary. <br>
Risk: If multiple PostHog accounts are linked, requests may affect or disclose data from the wrong connection. <br>
Mitigation: Choose the intended connection explicitly when multiple accounts are linked. <br>
Risk: Create, update, and delete-style API calls can change dashboards, insights, feature flags, cohorts, annotations, surveys, experiments, and related resources. <br>
Mitigation: Approve write operations only after checking the exact project, target resource, and intended effect. <br>


## Reference(s): <br>
- [ClawHub PostHog Skill](https://clawhub.ai/byungkyu/posthog-api) <br>
- [Maton](https://maton.ai) <br>
- [PostHog API Overview](https://posthog.com/docs/api) <br>
- [HogQL Documentation](https://posthog.com/docs/hogql) <br>
- [Feature Flags](https://posthog.com/docs/feature-flags) <br>
- [Session Replay](https://posthog.com/docs/session-replay) <br>
- [Experiments](https://posthog.com/docs/experiments) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API paths and inline Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; API responses are returned by the Maton-proxied PostHog service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
