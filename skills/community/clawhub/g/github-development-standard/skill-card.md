## Description: <br>
Guides agents through a GitHub development workflow with issue review, scoped implementation, local validation, diff review, release notes, and retrospectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SonicBotMan](https://clawhub.ai/user/SonicBotMan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill as a checklist for GitHub issue work, bug fixes, multi-file changes, verification, and release communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub CLI examples can post comments or close issues if copied with real repository and issue values. <br>
Mitigation: Confirm the repository, issue number, command intent, and authentication context before running GitHub CLI commands. <br>
Risk: Validation commands execute local project code or tests, which may have side effects in an untrusted repository. <br>
Mitigation: Run checks only in trusted workspaces or isolated environments and review project test behavior before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SonicBotMan/github-development-standard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with checklists and inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow guidance; no executable payload is included.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
