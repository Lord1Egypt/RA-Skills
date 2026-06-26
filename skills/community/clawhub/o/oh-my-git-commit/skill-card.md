## Description: <br>
Helps an agent create Conventional Commits by analyzing git diffs, staging selected changes, and generating Chinese commit messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoi-lau](https://clawhub.ai/user/hoi-lau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when they need to turn local git changes into a Conventional Commit. It guides diff review, logical staging, and commit message drafting before creating the commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage files and create commits, which may include secrets, unrelated files, or work in progress if changes are not reviewed. <br>
Mitigation: Review git status and diffs before staging or committing, and confirm that no sensitive or unrelated files are included. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hoi-lau/oh-my-git-commit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with Conventional Commit message text and optional git shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Chinese commit messages while keeping Conventional Commit type and scope labels in English.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
