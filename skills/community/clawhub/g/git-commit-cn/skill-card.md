## Description: <br>
Read git diff --staged, generate Conventional Commits format messages in Chinese. Requires: git. Shows diff summary, suggests commit type, generates message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill before committing staged Git changes to inspect the staged diff and draft a Chinese Conventional Commits message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Staged diffs can contain sensitive code, credentials, or unreleased business logic. <br>
Mitigation: Review staged files before invoking the skill and unstage or redact sensitive material before sharing the diff with an agent. <br>
Risk: The generated commit type or Chinese summary may not match the developer's intent. <br>
Mitigation: Use the displayed diff summary to verify the proposed Conventional Commits message before running git commit. <br>
Risk: The report template contains promotional affiliate links. <br>
Mitigation: Treat those links as visible promotional text and inspect the report before copying or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingaiwork/skills/git-commit-cn) <br>
- [Publisher homepage](https://kingai.work/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with a Chinese Conventional Commits message and optional git commit command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Git repository with staged changes; the developer should review the proposed message before committing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
