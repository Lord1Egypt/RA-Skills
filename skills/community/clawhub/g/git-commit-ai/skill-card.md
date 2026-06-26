## Description: <br>
Analyzes staged Git diffs and helps generate detailed Angular-style commit messages in Chinese or English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZenoLeee](https://clawhub.ai/user/ZenoLeee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill inside Git repositories to turn staged changes into concise, convention-compliant commit messages. It is most useful for teams that want richer commit descriptions, automatic Chinese or English language selection, and optional prepare-commit-msg hook reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Staged diffs can contain secrets, proprietary code, personal data, or internal URLs that may be included in AI analysis. <br>
Mitigation: Review git diff --cached before use and remove sensitive material from staged changes before asking the agent to analyze the diff. <br>
Risk: Installing the optional prepare-commit-msg hook changes repository behavior. <br>
Mitigation: Use --install only when a persistent commit reminder is desired and review any existing hook before accepting the change. <br>
Risk: Using --force with hook installation may replace an existing prepare-commit-msg hook. <br>
Mitigation: Check and back up existing hook behavior before running --install --force. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZenoLeee/git-commit-ai) <br>
- [Angular commit convention](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit) <br>
- [Git diff documentation](https://git-scm.com/docs/git-diff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with diff code fences, warnings, and commit-message guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include warnings about sensitive staged content or large diffs; install mode can modify the repository prepare-commit-msg hook.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
