## Description: <br>
Manage Git hooks with installation, configuration sharing, validation templates, and command-line or Python usage for repository workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to install, remove, list, export, import, and validate Git hooks that enforce linting, testing, branch naming, commit message, security scan, or local CI checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported hook configuration can install executable Git hooks that persist in a repository and run during later Git operations. <br>
Mitigation: Review imported hook JSON before use, accept configurations only from trusted sources, and remove unwanted files from .git/hooks when no longer needed. <br>
Risk: Pre-built hook templates can run local lint, test, audit, or security commands automatically as part of commit or push workflows. <br>
Mitigation: Install only templates that match the repository's intended workflow, pin dependencies, and document any required tools for contributors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/git-hooks-manager) <br>
- [Publisher profile](https://clawhub.ai/user/kaiyuelv) <br>
- [Artifact README](artifact/README.md) <br>
- [Basic usage example](artifact/examples/basic_usage.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, Python snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify executable Git hook files in a repository when its commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
