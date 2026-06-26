## Description: <br>
Simple command-line snippet manager. Use it to save and reuse complex commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumadeiras](https://clawhub.ai/user/gumadeiras) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to let an agent save, search, execute, and optionally sync reusable command-line snippets with the local pet CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved snippets may contain sensitive commands or secrets. <br>
Mitigation: Review snippets before saving, executing, or syncing them, and avoid storing tokens, passwords, or other credentials in pet snippets. <br>
Risk: Executing a saved snippet can run an unintended or stale shell command. <br>
Mitigation: Inspect the selected snippet before using pet exec, especially for commands that modify files, credentials, infrastructure, or remote services. <br>
Risk: Optional Gist sync can upload local snippets to GitHub. <br>
Mitigation: Use pet sync only when GitHub Gist upload is intended and the snippet contents are safe to share with the configured account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gumadeiras/pet) <br>
- [Publisher profile](https://clawhub.ai/user/gumadeiras) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and TOML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local pet CLI; snippets are stored in ~/.config/pet/snippet.toml and optional Gist sync can upload snippets to GitHub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
