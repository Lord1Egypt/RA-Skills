## Description: <br>
Guides agents through Git commits, pull requests, releases, conventional commit messages, changelog updates, and commit-message validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to prepare concise Git commits, create pull requests, tag releases, update changelogs, and validate commit-message format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to push commits to the configured remote immediately after committing. <br>
Mitigation: Before use, override the auto-push behavior so the agent must show the branch, remote, staged files, and active GitHub account before any push, tag, pull request, or release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/niracler/nini-git-workflow) <br>
- [Release v0.3.0 Changelog](https://github.com/niracler/skill/releases/tag/v0.3.0) <br>
- [Examples and Templates](references/examples-and-templates.md) <br>
- [Git Documentation](https://git-scm.com/) <br>
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and prose guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commit messages, pull request descriptions, release checklists, changelog guidance, and validation commands.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
