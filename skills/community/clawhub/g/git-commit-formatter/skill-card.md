## Description: <br>
Formats Git commit messages according to Conventional Commits v1.0.0 from git diffs, changed file lists, or text descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wipal](https://clawhub.ai/user/wipal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to turn a git diff, a list of changed files, or a natural-language change description into a Conventional Commit message with an appropriate type, optional scope, and optional body. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes unrelated whitelist instructions that could affect auto-add behavior if followed outside the commit-message workflow. <br>
Mitigation: Review or remove the whitelist section before installing, and use the skill only for commit-message generation. <br>
Risk: Git diffs and change descriptions may contain secrets, private keys, tokens, or sensitive proprietary code. <br>
Mitigation: Avoid pasting sensitive values or raw confidential diffs; redact secrets before using the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wipal/git-commit-formatter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Plain text or Markdown commit message with optional body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Subject line is limited to 50 characters; optional body lines are limited to 72 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
