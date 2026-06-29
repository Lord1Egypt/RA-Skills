## Description: <br>
Implements GitHub or GitLab issues via parallel subagents with review gates between task batches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to resolve one or more GitHub or GitLab issues end to end: fetch issue details, plan dependent work, run independent tasks in parallel, review changes, update issues, and prepare one consolidated pull request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to make repository changes and use authenticated GitHub or GitLab tooling. <br>
Mitigation: Run it only in a repository and branch where automated changes are acceptable, review the generated plan and diffs before merge, and keep issue closing disabled unless explicitly approved. <br>
Risk: The artifact includes a feedback step that can post tooling observations to the Night Market GitHub Discussions page. <br>
Mitigation: Disable or ignore that step unless the user explicitly approves the exact content and destination before posting. <br>
Risk: Automatic platform detection or Bitbucket references may not match the actual target platform. <br>
Mitigation: Confirm the target platform is GitHub or GitLab and verify the selected CLI commands before running issue updates. <br>
Risk: Parallel subagent execution can create conflicts, stalled sessions, or lost work if isolation modes are mixed. <br>
Mitigation: Use the artifact's conflict analysis, review gates, worktree checks, and local monitoring guidance before committing or merging parallel results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-do-issue) <br>
- [Configured homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, task plans, review prompts, configuration snippets, and issue or pull request text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead the agent to modify repository files, run tests, commit changes, update issue comments, and prepare a consolidated pull request.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
