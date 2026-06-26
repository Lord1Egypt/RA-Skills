## Description: <br>
Ship code with oneshot CLI: one command plans, executes, reviews, and opens a PR over SSH or locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adwilkinson](https://clawhub.ai/user/adwilkinson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate repository code changes to an automated pipeline that plans, implements, reviews, pushes a branch, and opens or updates a pull request. It supports local runs and trusted SSH-hosted runs for repositories with the required CLI credentials and tooling configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify selected repositories, push branches, and open or update pull requests using configured credentials. <br>
Mitigation: Use least-privilege GitHub and provider credentials, prefer dry-run or local mode first, and review generated plans, diffs, and PRs before merge. <br>
Risk: SSH mode can send active run configuration and Linear credentials to a remote host. <br>
Mitigation: Use SSH mode only with trusted hosts and avoid configuring credentials that are not required for the target workflow. <br>
Risk: Runs may execute long-lived automated coding, review, and PR workflows against a repository. <br>
Mitigation: Configure timeouts, use worktree isolation, inspect preserved failure worktrees and JSONL run logs, and start with dry-run validation for new repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adwilkinson/oneshot-ship) <br>
- [Publisher profile](https://clawhub.ai/user/adwilkinson) <br>
- [Oneshot CLI repository](https://github.com/ADWilkinson/oneshot-cli) <br>
- [Bun](https://bun.sh) <br>
- [Codex CLI](https://github.com/openai/codex) <br>
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or direct creation of pull requests, branches, commits, JSONL run events, policy files, and self-contained HTML artifacts during agent workflows.] <br>

## Skill Version(s): <br>
0.2.13 (source: server release metadata); 1.2.3 (source: artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
