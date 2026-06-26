## Description: <br>
PassManager provides a local SQLite-based password manager for AI assistant teams, with encrypted credential storage, role-based access controls, audit logging, and backup and restore commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isenlink](https://clawhub.ai/user/isenlink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI assistant operators use PassManager to store, retrieve, audit, and back up team credentials locally instead of relying on an external password-manager service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command-line secret exposure <br>
Mitigation: Do not use real credentials until secret entry avoids command-line arguments and shell history; prefer reviewed interactive input, protected files, or another approved secret-entry mechanism. <br>
Risk: Access control may be under-scoped for credential storage <br>
Mitigation: Review and test the role-based access-control implementation before storing sensitive data, including negative tests for unauthorized read, write, backup, restore, and team-management actions. <br>
Risk: Backup, restore, and export handling may expose credential material <br>
Mitigation: Confirm backup and export encryption, file permissions, retention, and restore behavior before enabling these commands with production credentials. <br>
Risk: Destructive or bulk operations may lack clear confirmation and recovery guidance <br>
Mitigation: Require explicit confirmations, recent recoverable backups, and documented recovery steps before allowing delete, restore, import, export, or bulk update workflows. <br>


## Reference(s): <br>
- [PassManager ClawHub Release](https://clawhub.ai/isenlink/passmanager) <br>
- [README](artifact/README.md) <br>
- [PassManager Skill Documentation](artifact/docs/passmanager_skill.md) <br>
- [PassManager Training Manual](artifact/docs/passmanager_training.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, Python code references, and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local SQLite database, audit log, backup, and configuration files under the configured PassManager data path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact files also mention 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
