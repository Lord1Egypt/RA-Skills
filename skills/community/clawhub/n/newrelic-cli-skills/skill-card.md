## Description: <br>
Monitor, query, and manage New Relic observability data via the newrelic CLI for NRQL queries, APM performance triage, deployment markers, alert management, infrastructure monitoring, and agent diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vince-winkintel](https://clawhub.ai/user/vince-winkintel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect New Relic observability data, triage application and infrastructure issues, record deployment markers, and manage alert configuration through the newrelic CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires New Relic account credentials and can read observability data from the configured account. <br>
Mitigation: Use a least-privilege New Relic user key scoped to the intended account and verify the active CLI profile before use. <br>
Risk: The skill includes workflows that can create deployment markers and alert configuration, and it documents alert condition deletion. <br>
Mitigation: Review proposed write commands before execution and manually confirm policy, condition, account, and application IDs before applying changes. <br>
Risk: Deleting an alert condition can reduce monitoring coverage. <br>
Mitigation: Require an explicit human confirmation step before running deletion commands and validate that replacement monitoring remains in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vince-winkintel/newrelic-cli-skills) <br>
- [Publisher profile](https://clawhub.ai/user/vince-winkintel) <br>
- [New Relic CLI](https://github.com/newrelic/newrelic-cli) <br>
- [New Relic CLI releases](https://github.com/newrelic/newrelic-cli/releases) <br>
- [NRQL query patterns](references/nrql-patterns.md) <br>
- [Performance triage guide](references/performance-triage.md) <br>
- [New Relic data exploration](https://one.newrelic.com/data-exploration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and New Relic CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured newrelic CLI profile and New Relic account credentials for live queries or write actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
