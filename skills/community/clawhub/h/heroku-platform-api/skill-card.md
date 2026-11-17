## Description:

Heroku Platform API helps agents manage the Heroku application lifecycle through HTTPS API calls using curl and jq, including apps, dynos, config vars, releases, add-ons, domains, logs, builds, pipelines, Postgres, maintenance, webhooks, review apps, and CI/CD workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imucyou](https://clawhub.ai/user/imucyou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and DevOps operators use this skill to inspect and manage Heroku apps without the Heroku CLI. It provides API-oriented guidance for read-only operations by default and gated write workflows for deployment, scaling, rollback, add-on, database, webhook, and CI/CD tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through Heroku operations affecting deployments, CI/CD, logs, backups, webhooks, and production resources.

Mitigation: Use the narrowest Heroku token scope available, keep HEROKU_PERMISSION=readonly by default, avoid global tokens, and manually review production-changing commands before execution.

Risk: Evidence security summary flags examples that may bypass the promised write-confirmation guard or fetch Heroku-returned URLs outside the stated network boundary.

Mitigation: Review generated commands before running them, especially log, deploy, backup, webhook, and any command that follows a returned URL; require external controls before enabling noninteractive writes.

Risk: Noninteractive write override can allow changes without a live confirmation prompt.

Mitigation: Do not set HEROKU_NONINTERACTIVE_WRITES unless a separate approval and audit process controls the run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imucyou/skills/heroku-platform-api)
- [Publisher profile](https://clawhub.ai/user/imucyou)
- [Project homepage](https://github.com/imucyou/heroku-platform-api)
- [Heroku account API key page](https://dashboard.heroku.com/account)
- [Heroku OAuth documentation](https://devcenter.heroku.com/articles/oauth)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash, curl, jq, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HEROKU_API_KEY, HEROKU_PERMISSION, curl, and jq; examples target api.heroku.com and postgres-api.heroku.com.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
