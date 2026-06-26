## Description: <br>
Heroku Platform API helps agents manage Heroku applications through audited HTTPS requests with curl and jq, including read-only defaults and guarded write operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imucyou](https://clawhub.ai/user/imucyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect and manage Heroku apps, dynos, config vars, releases, add-ons, domains, logs, builds, pipelines, Postgres resources, webhooks, review apps, and CI/CD workflows from an agent without requiring the Heroku CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent meaningful Heroku operational authority through a sensitive API token. <br>
Mitigation: Use a narrowly scoped read token first, keep HEROKU_PERMISSION=readonly unless changes are intended, and review operations before enabling full access. <br>
Risk: The security summary says the skill's safety and network-scope promises do not consistently match its examples. <br>
Mitigation: Review or patch examples so mutations go through the permission guard and returned URLs are host-validated before use. <br>
Risk: Logs, build output, source blobs, config values, and database backup URLs can expose sensitive Heroku data. <br>
Mitigation: Treat returned operational data as sensitive and avoid sharing it outside authorized workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imucyou/heroku-platform-api) <br>
- [Source homepage](https://github.com/imucyou/heroku-platform-api) <br>
- [Heroku OAuth documentation](https://devcenter.heroku.com/articles/oauth) <br>
- [Heroku account API key page](https://dashboard.heroku.com/account) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue Heroku API calls through curl and may write STATUS.md only during explicit multi-agent orchestration.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
