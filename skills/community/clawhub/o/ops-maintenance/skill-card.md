## Description: <br>
Ops Maintenance helps agents inspect local and remote systems, monitor server and cluster health, audit security posture, analyze logs, track configuration changes, manage alerts, run scheduled checks, inspect Docker container health, and monitor SSL certificates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to collect system health, security, log, Docker, SSL, alerting, and configuration-change information across local machines and configured remote servers. It is intended for environments where the agent is explicitly allowed to inspect systems, use SSH credentials, transfer files, and run approved operational checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use SSH credentials, run commands, transfer files, and affect production systems when connected to real infrastructure. <br>
Mitigation: Install it only where operational inspection is intended, use dedicated low-privilege SSH keys, restrict configured hosts and tags, and treat SFTP and cluster execution as production-impacting actions. <br>
Risk: Unsafe shell-command construction in several paths can increase command-injection or unintended-execution risk. <br>
Mitigation: Add confirmation gates, host and path allowlists, and safer non-shell command execution before using the skill on sensitive fleets. <br>
Risk: Alerting and webhook features can send operational information to configured destinations. <br>
Mitigation: Review webhook destinations and notification channel configuration before enabling alert delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fish1981bimmer/ops-maintenance) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [Release notes](artifact/RELEASE_NOTES.md) <br>
- [Security summary](artifact/SECURITY_SUMMARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, plain text, and inline shell or TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational findings, recommended commands, configuration snippets, reports, and audit or monitoring summaries.] <br>

## Skill Version(s): <br>
3.1.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
