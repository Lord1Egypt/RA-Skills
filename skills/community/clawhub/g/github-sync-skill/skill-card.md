## Description: <br>
Synchronizes locally created or modified Claude Code skills to a GitHub repository, with incremental sync, single-skill sync, token checks, and README generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuiilabs](https://clawhub.ai/user/kuiilabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to back up or publish selected local Claude Code skills to a GitHub repository and maintain a generated repository README. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A GitHub token with write access can create, update, or upload files in the target repository. <br>
Mitigation: Use a fine-grained token limited to the intended repository, avoid persistent broad token storage, and review the files under each selected skill before syncing. <br>
Risk: The cleanup script can recursively delete remote repository items that are not on its keep list. <br>
Mitigation: Run cleanup_remote_repo.sh with --dry-run first, review the deletion list, and execute deletion only when every unlisted remote item is intended to be removed. <br>
Risk: Broad sync behavior may publish unintended files from configured local skill directories. <br>
Mitigation: Review the configured skill whitelist and each selected skill directory before running sync_to_github.sh. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kuiilabs/github-sync-skill) <br>
- [Token troubleshooting guide](references/token-troubleshooting.md) <br>
- [GitHub personal access token documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) <br>
- [GitHub REST API rate limiting documentation](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, generated README content, and terminal sync reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke GitHub API operations using GITHUB_TOKEN and write repository files when bundled scripts are run.] <br>

## Skill Version(s): <br>
2.0.0 (source: server metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
