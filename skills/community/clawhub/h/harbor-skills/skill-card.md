## Description: <br>
Harbor Skills helps agents assist with Harbor registry administration, including projects, images, security scans, cleanup policies, CI/CD and GitOps integration, replication, storage, backups, recovery, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiutoo](https://clawhub.ai/user/qiutoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and operations teams use this skill to generate Harbor administration guidance, API calls, scripts, and configuration examples for registry operations, cleanup, compliance checks, robot accounts, backup and recovery, and automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review identifies this as a real Harbor administration skill with production-impacting examples and weak guardrails. <br>
Mitigation: Review every delete, garbage collection, replication, restore, webhook, GitOps, and account-management action before running it against a Harbor instance. <br>
Risk: The skill requires sensitive Harbor credentials and includes examples that can expose or print tokens. <br>
Mitigation: Use least-privilege robot accounts with expirations, avoid admin passwords and inline secrets, and treat scan reports, audit logs, backups, and webhook payloads as sensitive production data. <br>
Risk: Cleanup, restore, and robot-account scripts can delete registry artifacts, alter credentials, or affect recovery state. <br>
Mitigation: Run dry-run modes first, verify exclusions and backup coverage, require operator confirmation, and test recovery procedures before making destructive changes. <br>


## Reference(s): <br>
- [Harbor API v2.0 Reference](references/harbor-api.md) <br>
- [Cleanup Policy](references/cleanup-policy.md) <br>
- [Backup and Recovery](references/backup-recovery.md) <br>
- [GitOps Integration](references/gitops.md) <br>
- [Webhook](references/webhook.md) <br>
- [Compliance](references/compliance.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/qiutoo/harbor-skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands, API examples, Python snippets, JSON, YAML, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include production-impacting Harbor API and Docker commands that require review before execution.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence; artifact frontmatter reports 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
