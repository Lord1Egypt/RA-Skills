## Description:

Helps agents inspect Netlify sites, deploys, builds, DNS, and environment variables, with approval required for changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site administrators use this skill to review Netlify resources and deployment status, or to make explicitly approved changes through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account can grant broad access to Netlify resources.

Mitigation: Review OAuth scopes and connect only the account and permissions needed for the task.

Risk: Site, DNS, environment-variable, or membership changes can disrupt services or expose sensitive data.

Mitigation: Prefer read-only work; show the target and impact, then obtain explicit approval before each change.

Risk: Build hooks, webhooks, and triggers can create persistent automation or forward data.

Mitigation: Require separate, explicit approval before creating hooks, destinations, or other persistent automation.

## Reference(s):

- [ClawHub Netlify skill](https://clawhub.ai/byungkyu/skills/netlify-api)
- [Maton](https://maton.ai)
- [Netlify API documentation](https://open-api.netlify.com/)
- [Maton documentation](https://docs.maton.ai)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with API results and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the connected account's permissions; changes require explicit approval.]

## Skill Version(s):

1.2.7 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
