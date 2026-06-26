## Description: <br>
Publish the current project to a GitHub remote repository, including Git initialization, remote setup, automatic commits, and pushing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orbisz](https://clawhub.ai/user/orbisz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to publish a local project to a GitHub repository from an agent session. It helps initialize Git when needed, configure or reuse a remote, commit pending changes, push the current branch, and remember repository mappings for later use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage all files, create commits, configure remotes, and push to GitHub, which may publish secrets or unrelated local changes. <br>
Mitigation: Inspect git status and diffs before use, remove secrets or unrelated files, and confirm the remote URL before allowing commits or pushes. <br>
Risk: The workflow offers force-push after non-fast-forward failures, which can overwrite remote history. <br>
Mitigation: Use normal push first and approve force-push only when the remote history impact is understood and intentional. <br>
Risk: The artifact includes persistent repository mapping and self-evolution diary/PR behavior that may record project paths or change skill behavior over time. <br>
Mitigation: Review or remove repo-map persistence and the self-evolution section before deployment if persistent local path storage or self-modification is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orbisz/git-publish-skill) <br>
- [Repository mapping reference](references/repo-map.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and commit-message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify repository state by staging files, creating commits, setting remotes, pushing branches, and updating a local repo-map reference.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
