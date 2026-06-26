## Description: <br>
Implements GitHub or GitLab issues via parallel subagents with review gates between task batches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to retrieve forge issues, break them into implementation tasks, coordinate parallel or sequential work, run review gates, and prepare issue updates or a consolidated pull request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to post tooling feedback to an unrelated Night Market GitHub Discussions repository without an explicit approval gate. <br>
Mitigation: Disable that feedback step or require explicit user confirmation before any external discussion post. <br>
Risk: The workflow can prepare issue comments and optionally close issues through forge CLI commands. <br>
Mitigation: Review all proposed comments and closures before they are posted, and keep automatic issue closing disabled unless the user has approved it. <br>
Risk: Broad automatic activation in sensitive repositories could let the agent make or coordinate substantial code changes. <br>
Mitigation: Use the skill on a dedicated branch, limit concurrent workers, inspect diffs, and run the relevant tests before creating or merging a pull request. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/athola/nm-sanctum-do-issue) <br>
- [Project homepage from metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>
- [Issue discovery module](artifact/modules/issue-discovery.md) <br>
- [Parallel execution module](artifact/modules/parallel-execution.md) <br>
- [Completion module](artifact/modules/completion.md) <br>
- [Troubleshooting module](artifact/modules/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples, task plans, code-review prompts, and issue-update commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate subagents or agent teams and may use GitHub or GitLab CLI commands to read, comment on, or close issues.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
