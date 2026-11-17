## Description:

Integrated memory management and extreme context compression for OpenClaw, combining memory management, compression, search, and automation in one unified skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hassffw](https://clawhub.ai/user/hassffw)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to compress, manage, search, and clean up OpenClaw memory files, including scheduled compression and local health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation or enablement can create recurring background OpenClaw execution that reads and processes local memory without a separate opt-in.

Mitigation: Install only when recurring memory compression is intended, inspect the created cron job, verify the memory and data directories it touches, and confirm scheduled jobs can be removed manually if needed.

Risk: Compression and cleanup scripts operate on local memory, data, backup, and log files.

Mitigation: Review configuration before running scripts, keep backups enabled, and use documented dry-run or status commands before cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hassffw/skills/memory-compression-system)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local skill data, configuration, logs, backups, and scheduled OpenClaw jobs when its scripts are run.]

## Skill Version(s):

3.0.1 (source: server release metadata; artifact frontmatter and package.json report 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
