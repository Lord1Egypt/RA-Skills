## Description:

仓库归档专业版 helps agents archive and monitor GitHub repositories, cluster duplicate issues, schedule repository syncs, coordinate shared archive storage, and prepare repository health or alerting outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering teams, and open-source maintainers use this skill to manage multi-repository archives, identify duplicate issues, keep repository data synchronized, and produce operational reports or PR status alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or mismatched trigger language could cause repository, file, command, GitHub, or webhook workflows to run in unintended contexts.

Mitigation: Use the skill only for explicit repository archiving, monitoring, issue or PR analysis, and team sync tasks; avoid activating it for SEO, marketing, or generic coding help.

Risk: Command execution, scheduled syncs, GitHub-token use, shared storage, or webhook notifications may affect local files, external services, or team data.

Mitigation: Confirm Bash commands, schedules, shared storage paths, GitHub-token scope, and webhook destinations before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/gitcrawl-tool-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured text with inline bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository lists, sync settings, clustering parameters, webhook configuration guidance, health reports, and execution-log style JSON results.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
