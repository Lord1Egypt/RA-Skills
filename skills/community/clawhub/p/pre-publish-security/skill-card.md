## Description: <br>
Pre Publish Security provides frequency-aware security audits for GitHub and ClawHub releases, checking for credential leaks, dependency vulnerabilities, documentation issues, and risky pushes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solmas](https://clawhub.ai/user/solmas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to scan repositories before publishing, catch leaked credentials, dependency vulnerabilities, documentation placeholders, and license or README gaps, and optionally install a pre-push hook that blocks risky pushes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change git push behavior by installing a pre-push hook that blocks pushes when checks fail. <br>
Mitigation: Install it only on intended repositories, review and back up any existing .git/hooks/pre-push file first, and test the audit command manually before relying on the hook. <br>
Risk: Local audit reports and terminal output may include sensitive findings or secret snippets from scanned repositories. <br>
Mitigation: Run it only on repositories whose scan scope is acceptable, keep reports local, and delete /tmp security audit reports after review. <br>
Risk: Dependency and history scans may inspect broad repository content and optional package ecosystems. <br>
Mitigation: Confirm optional tools and scan modes match the repository policy before running full, history, or dependency audits. <br>


## Reference(s): <br>
- [Pre Publish Security on ClawHub](https://clawhub.ai/solmas/pre-publish-security) <br>
- [README](artifact/README.md) <br>
- [Security Audit Schedule](artifact/AUDIT-SCHEDULE.md) <br>
- [Project homepage listed in skill metadata](https://github.com/solmas/openclaw-pre-publish-security) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Terminal output and Markdown reports with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update audit-state.json, write local audit reports under /tmp, and install a git pre-push hook when invoked.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
