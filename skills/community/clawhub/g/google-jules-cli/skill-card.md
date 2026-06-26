## Description: <br>
Interface with Google's Jules Tools CLI to manage AI coding sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexdavidswift](https://clawhub.ai/user/alexdavidswift) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to help an agent install, authenticate, and operate the Google Jules CLI for remote AI coding sessions, including listing sessions, starting tasks, and pulling completed changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the Jules CLI globally can require elevated npm permissions. <br>
Mitigation: Prefer a normal user-level npm install and ask the user before using sudo or changing system-level package locations. <br>
Risk: Jules authentication connects the agent workflow to a Google account. <br>
Mitigation: Authenticate only with the intended account and log out or re-authenticate if account context is unclear. <br>
Risk: Pulling Jules session results can modify repository files. <br>
Mitigation: Pull results on a clean branch or disposable clone, then review `git status` and diffs before committing, merging, or deploying. <br>


## Reference(s): <br>
- [Google Jules CLI Reference](https://jules.google/docs/cli/reference/) <br>
- [ClawHub Skill Page](https://clawhub.ai/alexdavidswift/google-jules-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, code] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide Jules CLI sessions that pull code changes into a repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
