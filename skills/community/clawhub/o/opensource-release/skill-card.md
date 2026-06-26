## Description: <br>
Convert a private repository to public open-source by scanning for personal data, checking cached artifacts, cleaning Git history, changing repository visibility, and verifying the public release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jini92](https://clawhub.ai/user/jini92) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill when preparing a private repository for open-source publication, including source and documentation scans, history cleanup decisions, repository visibility changes, and post-release checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes force-push and branch-deletion commands that can erase Git history. <br>
Mitigation: Confirm the target GitHub account, owner/repo, current branch, backup or mirror clone, and sanitized repository contents before running destructive Git commands. <br>
Risk: The skill includes repository visibility-change guidance that can expose private code publicly. <br>
Mitigation: Complete source, documentation, cached-artifact, secret, and remote URL checks before changing repository visibility to public. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jini92/opensource-release) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jini92) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown checklist with inline PowerShell, Git, and GitHub CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on repository release preparation, sensitive-data review, Git history cleanup choices, and visibility verification.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
