## Description: <br>
A comprehensive Git command assistant and workflow guide. Trigger whenever the user asks how to perform a specific Git operation, wants to know what a Git command does, needs help fixing a Git mistake, or wants guidance on Git best practices (like branching, rebasing, or squashing). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny0826](https://clawhub.ai/user/sunny0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to get Git command explanations, workflow guidance, recovery steps, and safer command options in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested destructive Git commands could cause data loss when used on the wrong repository state. <br>
Mitigation: Review commands before running them, check repository state with commands such as git status or git log, and make backups before reset, clean, rebase, amend, or force-push operations. <br>
Risk: History-rewriting guidance can disrupt shared branches if applied after commits have been pushed. <br>
Mitigation: Confirm whether the branch is shared or public before rewriting history, prefer non-rewriting alternatives when appropriate, and use force-with-lease only after reviewing the remote state. <br>
Risk: Guidance for accidentally committed secrets may be incomplete if credentials remain active after repository cleanup. <br>
Mitigation: Revoke or rotate exposed credentials first, then use appropriate history-cleanup tools and verify that the secret is no longer present. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunny0826/git-helper-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with fenced bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English or Chinese output based on the user's prompt language.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
