## Description:

Rosette Text Analytics (babelstreet.com). Use this skill for ANY Rosette Text Analytics request — searching and reading data. Whenever a task involves Rosette Text Analytics, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the OOMOL-connected Rosette service to analyze text for sentiment, entities, categories, language, and tokens. The skill guides them to check each action's schema and submit a matching request through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unchecked oo CLI installation may make persistent changes to agent skill directories.

Mitigation: Install a verified, fixed CLI release and review its persistent changes; set OO_SKILLS_SYNC_DISABLED=1 to prevent startup writes to agent skill directories.

Risk: Text sent for analysis is processed by OOMOL and Rosette Text Analytics.

Mitigation: Submit only text that you are authorized to share with both services.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Rosette Text Analytics documentation](https://documentation.babelstreet.com/analytics/text-analytics)
- [Babel Street Insights](https://www.babelstreet.com/babel-street-insights)
- [oo CLI environment options](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Shell commands]

**Output Format:** [JSON requests and structured text-analysis results, with Markdown instructions and inline Bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Request payloads must match the live schema for the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
