## Description: <br>
Secure GitHub push automation with auto SSH and remote config. Use when git push, automated push, or conflict handling needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NimaChu](https://clawhub.ai/user/NimaChu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to prepare and push local files to GitHub repositories with automated SSH detection, remote setup, commit creation, and conflict handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite local repository state and remove existing Git metadata during automated setup. <br>
Mitigation: Run it only in disposable or intentionally prepared directories, and keep backups or a separate clone before execution. <br>
Risk: The skill can use locally available SSH credentials automatically. <br>
Mitigation: Use a dedicated GitHub key with limited scope, verify the selected identity before pushing, and avoid running it where sensitive keys are loaded. <br>
Risk: The skill can force-push, which may overwrite remote history on shared repositories. <br>
Mitigation: Run --dry-run first, verify the target repository and branch, and avoid --force unless the repository is private or coordinated with collaborators. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/NimaChu/github-push) <br>
- [API Reference](references/api.md) <br>
- [Configuration Guide](references/configuration.md) <br>
- [Usage Examples](references/examples.md) <br>
- [Anti-Patterns Guide](references/anti-patterns.md) <br>
- [Security Notice](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and Python CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local Git and SSH operations when an agent follows the skill.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
