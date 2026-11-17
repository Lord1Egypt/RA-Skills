## Description:

This skill helps agents manage and optimize Ocean Engine advertising workflows, including campaign operations, reports, automated launch flows, budget suggestions, creative testing, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqzzzqa](https://clawhub.ai/user/aqzzzqa)

### License/Terms of Use:

MIT-0

## Use Case:

Advertising optimization teams, digital marketing managers, media buyers, and engineers use this skill to manage Ocean Engine ad accounts, inspect campaign reports, generate optimization recommendations, and automate budget or launch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify live Ocean Engine ads and budgets.

Mitigation: Use a test account first, keep budgets capped, and require review before production actions.

Risk: OAuth credentials and account tokens can grant ad account access.

Mitigation: Use environment variables, protect tokens, and avoid save_config() until credential storage is fixed.

Risk: Dependencies and API clients run with local environment access.

Mitigation: Install and execute the skill in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aqzzzqa/skills/oceanengine-ads)
- [Ocean Engine developer platform](https://developer.oceanengine.com/)
- [Ocean Engine](https://oceanengine.com)
- [LemClaw homepage](https://www.lemclaw.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, CLI text, JSON-like API results, generated reports, and Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Ocean Engine ad resources when configured with account credentials; optimization reports can be saved as local text files.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact documentation lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
