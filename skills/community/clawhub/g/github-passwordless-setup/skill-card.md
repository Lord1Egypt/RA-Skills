## Description: <br>
Complete GitHub passwordless authentication setup using SSH keys and Personal Access Tokens. Never type passwords or re-authenticate for Git operations and GitHub API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happydog-intj](https://clawhub.ai/user/happydog-intj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure GitHub SSH key authentication and GitHub CLI Personal Access Token access for passwordless Git operations, repository management, and issue or pull request workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill asks users to run unpinned remote code. <br>
Mitigation: Inspect the scripts locally before execution and avoid the curl-to-bash quick start. <br>
Risk: The security summary says the skill can grant broad, long-lived GitHub access. <br>
Mitigation: Use a fine-grained expiring GitHub token with only the required scopes, and avoid delete_repo or admin:org unless specifically needed. <br>
Risk: The security guidance warns that verification can create or delete repositories. <br>
Mitigation: Run repository create/delete verification only on a disposable or non-critical GitHub account. <br>
Risk: Artifact behavior includes token entry and optional token environment configuration. <br>
Mitigation: Do not persist Personal Access Tokens in shell startup files, and rotate or revoke unused tokens regularly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/happydog-intj/github-passwordless-setup) <br>
- [GitHub SSH documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) <br>
- [GitHub CLI manual](https://cli.github.com/manual/) <br>
- [GitHub CLI Linux installation documentation](https://github.com/cli/cli/blob/trunk/docs/install_linux.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and setup scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional shell scripts for setup and verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
