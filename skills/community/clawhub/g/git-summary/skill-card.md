## Description: <br>
Get a quick summary of the current Git repository including status, recent commits, branches, and contributors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zweack](https://clawhub.ai/user/zweack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a local Git repository and produce a concise repository summary covering status, commits, branches, remotes, uncommitted changes, and contributors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated summaries can expose sensitive repository metadata, including remote URLs, commit messages, branch names, contributor names, and changed file paths. <br>
Mitigation: Review summaries before sharing them externally and redact secrets, tokens, private URLs, or sensitive project details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zweack/git-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown summary with Git command results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git on darwin, linux, or win32; summaries may include repository metadata such as remote URLs, commit messages, branch names, contributor names, and changed file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
