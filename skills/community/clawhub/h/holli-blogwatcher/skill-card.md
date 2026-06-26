## Description: <br>
Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollis9087](https://clawhub.ai/user/hollis9087) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install blogwatcher and ask an agent for CLI commands to track RSS/Atom feeds, scan for new articles, list articles, and mark entries as read. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install guidance uses a Go module with @latest, so installed code can change over time. <br>
Mitigation: Review the upstream project before installing or pin a specific module version for repeatable installs. <br>
Risk: The skill relies on an external CLI and user-provided blog or RSS/Atom feed URLs. <br>
Mitigation: Install the CLI from a trusted source and review feed URLs before adding them to tracking. <br>


## Reference(s): <br>
- [Blogwatcher GitHub repository](https://github.com/Hyaxia/blogwatcher) <br>
- [ClawHub skill page](https://clawhub.ai/hollis9087/holli-blogwatcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance assumes the blogwatcher binary is installed and available on PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
