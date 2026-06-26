## Description: <br>
Secure GitHub push automation with auto SSH and remote config for git push, automated push, and conflict handling workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to prepare SSH-backed GitHub pushes, configure a remote, stage and commit local files, run dry runs, and retry failed pushes with rebase or optional force push behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can delete local Git history and rewrite repository state when it reinitializes a directory or uses force push behavior. <br>
Mitigation: Use it only on disposable or backed-up directories, run dry-run first, inspect the target remote and file list, and avoid force push on shared branches. <br>
Risk: Automated pushes may upload files that should not leave the local environment if the selected path contains secrets or private data. <br>
Mitigation: Avoid paths containing secrets, review the dry-run output before pushing, and keep sensitive files outside the upload path even though the artifact includes exclusion patterns. <br>
Risk: Automatic remote configuration and conflict handling can push to the wrong repository or obscure upstream changes if inputs are incorrect. <br>
Mitigation: Verify the repository owner/name, SSH access, current branch state, and remote URL manually before allowing a real push. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/github-push-cn) <br>
- [GitHub Push API Reference](references/api.md) <br>
- [GitHub Push Configuration Guide](references/configuration.md) <br>
- [GitHub Push Examples](references/examples.md) <br>
- [GitHub Push Anti-Patterns Guide](references/anti-patterns.md) <br>
- [GitHub Push Security Notice](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, Python examples, and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on local Git state and can push to a GitHub remote; dry-run should be used before any real push.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml; script reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
