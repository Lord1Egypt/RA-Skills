## Description:

Auto-fixes security vulnerabilities in OpenClaw skills by remediating hardcoded secrets, shell injection risks, prompt injection, and path traversal issues while generating secure replacements and environment variable templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to generate and apply fixes for vulnerabilities reported in OpenClaw skills, including secrets handling, shell command execution, prompt injection, and path traversal patterns. It supports dry-run review, interactive application, environment template generation, and fix reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-fix mode may corrupt code or write outside the intended target.

Mitigation: Use the skill only on a clean, backed-up repository; prefer --dry-run; inspect every diff manually; and avoid --auto until path containment and source-replacement issues are fixed.

Risk: Unattended fixes may bypass manual review for changes that need human judgment.

Mitigation: Use interactive mode for normal review workflows, keep backups enabled, and rescan and test the skill after any generated change is applied.

Risk: The release security verdict is suspicious due to unsafe file-modification behavior.

Mitigation: Treat the skill as an untrusted third-party remediation tool and run it in an isolated workspace before using it on sensitive repositories.

## Reference(s):

- [Fix Templates](references/fix-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/neckr0ik/skills/neckr0ik-security-fixer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, JSON reports, and generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify target skill files, create .bak backups, generate .env.example, and update .gitignore when fixes are applied.]

## Skill Version(s):

1.0.0 (source: frontmatter and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
