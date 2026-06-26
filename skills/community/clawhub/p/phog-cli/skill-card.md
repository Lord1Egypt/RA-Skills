## Description: <br>
Manage PostHog product analytics from the terminal for analytics, feature flags, experiments, surveys, dashboards, insights, logs, queries, and product health metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nelsongallardo](https://clawhub.ai/user/nelsongallardo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent run or suggest PostHog CLI workflows for product analytics reporting, HogQL queries, and administration of feature flags, experiments, surveys, dashboards, insights, logs, and related resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to change or delete PostHog resources, skip confirmations, and use raw API write or delete calls. <br>
Mitigation: Use a least-privilege PostHog token, prefer test or read-only credentials where possible, and require explicit review before any --yes command, delete, rollout change, experiment launch or end, or raw API POST, PATCH, or DELETE call. <br>
Risk: PostHog credentials and project configuration can expose product analytics data or administrative access. <br>
Mitigation: Scope credentials to the needed project and task, keep tokens out of shared logs and prompts, and store local CLI configuration with restrictive permissions. <br>


## Reference(s): <br>
- [Complete Command Reference](references/commands.md) <br>
- [ClawHub Release Page](https://clawhub.ai/nelsongallardo/phog-cli) <br>
- [Repository Metadata](https://github.com/nelsongallardo/posthog-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-reference text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend JSON output for programmatic parsing of PostHog CLI responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
