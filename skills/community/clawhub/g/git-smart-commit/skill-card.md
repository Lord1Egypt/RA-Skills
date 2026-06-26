## Description: <br>
Analyze staged git changes and generate high-quality commit messages following Conventional Commits format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wusuiling-if](https://clawhub.ai/user/wusuiling-if) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect staged Git changes, draft Conventional Commits messages, and optionally create a commit after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository diffs may include sensitive code, accidental secrets, or private implementation details. <br>
Mitigation: Invoke the skill only in repositories where staged changes may be inspected, and review the generated message before sharing or committing it. <br>
Risk: A generated commit message may misrepresent the change or hide unrelated changes in a single commit. <br>
Mitigation: Review the proposed message against the staged diff and split unrelated changes with git add -p when the skill recommends doing so. <br>
Risk: The skill can produce a git commit command after approval. <br>
Mitigation: Require explicit user approval before running git commit, and use dry-run message generation when only wording is needed. <br>


## Reference(s): <br>
- [Conventional Commits](https://www.conventionalcommits.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline git commands and Conventional Commits message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a subject-only commit message, an optional body/footer, split-commit guidance, or a proposed git commit command when the user approves committing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
