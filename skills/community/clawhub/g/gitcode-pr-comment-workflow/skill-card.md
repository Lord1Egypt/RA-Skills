## Description: <br>
GitCode PR review comment response workflow that accepts a PR link, fetches review comments, checks out the PR source branch, proposes and applies confirmed changes, pushes updates, and helps reply to unaddressed comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guitenbay](https://clawhub.ai/user/guitenbay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to work through GitCode pull request review comments, plan confirmed changes, update the PR source branch, and respond to comments that remain out of scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can push commits and post GitCode PR comments. <br>
Mitigation: Require explicit user confirmation before modifying files, committing, pushing, or posting PR replies, and verify the target branch and remote before each external write. <br>
Risk: GitCode access tokens may be exposed through URL-based API calls, logs, shell history, screenshots, or shared transcripts. <br>
Mitigation: Prefer authenticated CLI commands or safer header-based token handling, avoid placing tokens in visible command strings, and scrub transcripts and temporary files that may contain credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guitenbay/gitcode-pr-comment-workflow) <br>
- [gitcode-api.md](references/gitcode-api.md) <br>
- [GitCode CLI](https://github.com/codeasier/gitcode-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, design notes, diffs, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate temporary workflow files under temp/ and proposes external writes, commits, pushes, and PR replies only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
