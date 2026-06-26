## Description: <br>
Run Kilo CLI via background process for programmatic control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codewithnathan97](https://clawhub.ai/user/codewithnathan97) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to run Kilo CLI as a supervised background coding agent for code generation, pull request review, issue fixing, and GitHub workflow support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background coding agents can execute commands and make GitHub changes with the user's token. <br>
Mitigation: Use the narrowest possible GitHub token, supervise sessions, and review generated comments, pushes, and pull requests before publishing. <br>
Risk: Agent output or session logs may expose secrets, private prompts, internal URLs, or sensitive implementation details. <br>
Mitigation: Run in an isolated temporary clone or worktree and remove sensitive content from PR text, comments, and logs before sharing. <br>


## Reference(s): <br>
- [Kilo CLI Coding Agent on ClawHub](https://clawhub.ai/codewithnathan97/kilocli-coding-agent) <br>
- [GitHub CLI installation](https://github.com/cli/cli#installation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and PR review text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated code changes, GitHub PR comments, branch or worktree instructions, and session monitoring guidance.] <br>

## Skill Version(s): <br>
0.0.9 (source: frontmatter, claw.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
