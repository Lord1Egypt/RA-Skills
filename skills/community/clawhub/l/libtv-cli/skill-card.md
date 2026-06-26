## Description: <br>
Guides agents in using the LibTV CLI to install and authenticate the tool, manage LibTV canvas projects, nodes, groups, models, uploads, and media generation workflows from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taosiuman](https://clawhub.ai/user/taosiuman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to operate LibTV canvas workflows through documented CLI commands instead of manual HTTP calls or web-only steps. It supports project setup, account login, node creation and updates, asset uploads, grouping, piping, and media generation runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads a platform-specific LibTV CLI archive from the LibTV distribution host and may update the user's PATH. <br>
Mitigation: Install only when the distribution host is trusted, prefer the bundled installer from the skill directory, and use the documented skip-profile options when PATH changes are not desired. <br>
Risk: Login writes session credentials to ~/.libtv/credentials.json or to the configured LibTV credential directory. <br>
Mitigation: Treat the credentials file as sensitive, keep it out of synced or committed directories, and use an isolated credential directory when separating accounts or environments. <br>
Risk: Upload and generation commands can send local files, prompts, and workflow settings to LibTV services. <br>
Mitigation: Review files, prompts, model settings, and command output before upload or generation. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/taosiuman/libtv-cli) <br>
- [LibTV web application](https://www.liblib.art/tv/zh) <br>
- [LibTV CLI latest manifest](https://liblibai-web-static.liblib.cloud/cli/latest/manifest.json) <br>
- [Skill documentation map](SKILL.md) <br>
- [Installer documentation](scripts/install.md) <br>
- [Workflow examples](examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with shell command examples and JSON or NDJSON output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command references, installation notes, authentication guidance, workflow examples, and node/model schema guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
