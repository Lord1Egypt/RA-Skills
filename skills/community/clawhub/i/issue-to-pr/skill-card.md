## Description: <br>
Issue To Pr helps an agent read a GitHub issue, analyze the target repository, implement a fix, verify the change, and prepare a pull request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ydx3906](https://clawhub.ai/user/4ydx3906) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to turn a GitHub issue reference into a local fix workflow, including issue triage, repository analysis, code changes, verification, and pull request preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the user's GitHub CLI identity to access repositories, fork projects, push branches, and create pull requests. <br>
Mitigation: Use it only with GitHub access you are comfortable delegating, confirm the target repository, and require explicit approval before forking, pushing, or opening a pull request. <br>
Risk: The workflow may run project test, lint, or build commands from the target repository. <br>
Mitigation: Review commands before execution and prefer an isolated checkout or sandbox when working with untrusted repositories. <br>
Risk: The agent modifies local source files while attempting to fix an issue. <br>
Mitigation: Inspect the root cause analysis and diff before commit or PR creation, and keep unrelated local work out of the working tree. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/4ydx3906/issue-to-pr) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks, code edits, commit messages, and pull request text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May clone repositories, edit local files, run project checks, and create branches or pull requests after user confirmation.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter, changelog, clawhub.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
