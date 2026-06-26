## Description: <br>
Generate, install, and manage Git hooks with pre-built templates for linting staged files, enforcing commit conventions, blocking debug statements, preventing large file commits, formatting code, requiring ticket references, protecting branches, running tests, and installing dependencies after merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to list, preview, install, check, and remove repository-local Git hook templates that enforce common commit, linting, formatting, testing, branch-protection, and dependency-update workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installed Git hooks run local tools automatically during repository workflows. <br>
Mitigation: Preview each template before installing it and install hooks only in repositories where that automation is intended. <br>
Risk: Using --force can replace an existing hook. <br>
Mitigation: Avoid --force unless replacing the current hook is intentional, and review or back up the existing hook first. <br>
Risk: The post-merge dependency template can run package-manager install commands after future merges. <br>
Mitigation: Use the post-merge dependency hook only in trusted repositories and review dependency or lockfile changes before merging. <br>


## Reference(s): <br>
- [Git Hooks Toolkit on ClawHub](https://clawhub.ai/Johnnywang2001/git-hooks-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated Git hook script content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates executable repository-local Git hook files under .git/hooks when installation commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, created 2026-03-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
