## Description: <br>
Run an autonomous Open Ralph Wiggum coding loop using OpenCode Zen with free models and automatic fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bderiel](https://clawhub.ai/user/Bderiel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run bounded autonomous coding loops for fixing tests, implementing scoped features, refactoring, resolving lint or type errors, and iterating on build failures inside a git repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an autonomous local coding agent to modify repository files over multiple iterations. <br>
Mitigation: Run it on a clean branch or worktree, keep iteration limits conservative, and review the full git diff before committing or merging. <br>
Risk: Prompts and repository context may be processed by OpenCode or its configured model providers. <br>
Mitigation: Avoid private code or secrets unless that provider processing is acceptable for the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bderiel/open-ralph) <br>
- [Skill metadata homepage](https://github.com/Th0rgal/open-ralph-wiggum) <br>
- [OpenCode Zen models](https://opencode.ai/zen/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for running Ralph with bounded iterations, completion criteria, fallback models, and troubleshooting flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
