## Description:

Queries Brazilian judicial processes through the public DataJud API from Brazil's National Council of Justice.

This skill is for research and development only.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to look up Brazilian public court cases by CNJ number, search cases by court filters, infer tribunal aliases, and monitor case movement updates.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: Credential handling may expose a private DATAJUD_API_KEY during dry runs because request headers can be printed.

Mitigation: Review before installing and avoid dry-run mode with a private DATAJUD_API_KEY unless Authorization headers are redacted.

Risk: Monitored CNJ case numbers and movement snapshots are retained in a local state file.

Mitigation: Treat monitored case numbers as sensitive local data and prefer a version that clearly documents or lets users configure the monitoring state file.

Risk: The security verdict is suspicious due to review-worthy credential handling and local retention issues.

Mitigation: Prefer a version that removes the embedded key and masks headers before deployment.

## Reference(s):

- [DataJud Public API](https://api-publica.datajud.cnj.jus.br/)
- [ClawHub skill page](https://clawhub.ai/runawaydevil/skills/klaus-processos-br)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or JSON CLI output, with Markdown-formatted usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make network requests to the DataJud public API and may store monitored case numbers and movement snapshots in a local JSON state file.]

## Skill Version(s):

0.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
