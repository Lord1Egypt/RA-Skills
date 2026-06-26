## Description: <br>
AutoGitHub helps agents manage GitHub repositories, review pull requests, generate changelogs, set up CI/CD workflows, manage issues, and support project automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiiyyo](https://clawhub.ai/user/shiiyyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use AutoGitHub to automate routine GitHub repository operations such as repository setup, pull request review, changelog generation, issue handling, and workflow configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool handles powerful GitHub credentials and stores configuration locally. <br>
Mitigation: Use a fine-grained GitHub token limited to intended repositories, protect .github-manager.json, and keep real tokens out of shared shells, logs, and version control. <br>
Risk: The changelog flow includes a local command path that can be unsafe with untrusted tags or --since values. <br>
Mitigation: Only run changelog generation in trusted repositories and avoid untrusted tag or --since input. <br>
Risk: Generated GitHub Actions workflows can affect repository automation and deployment behavior. <br>
Mitigation: Inspect generated workflow files before committing them and verify permissions, secrets, and deployment triggers. <br>


## Reference(s): <br>
- [AutoGitHub on ClawHub](https://clawhub.ai/shiiyyo/github-manager) <br>
- [README.md](artifact/README.md) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Terminal text and Markdown, with generated JSON and GitHub Actions YAML files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local GitHub configuration, changelog, and workflow files in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
