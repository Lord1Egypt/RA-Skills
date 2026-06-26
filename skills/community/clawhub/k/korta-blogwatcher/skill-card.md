## Description: <br>
Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[landercortazarromero](https://clawhub.ai/user/landercortazarromero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and operate the blogwatcher CLI for tracking blog and RSS/Atom feed updates, scanning configured feeds, and managing read or unread article status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install command uses the latest Go module version, which can reduce reproducibility. <br>
Mitigation: Pin a specific Go module version when reproducible installs or change control are required. <br>
Risk: The CLI contacts blog or RSS/Atom feed URLs configured by the user. <br>
Mitigation: Configure only feeds you intend to contact from the current environment and review network expectations before scanning. <br>
Risk: The CLI keeps local tracking state for articles and read status. <br>
Mitigation: Treat the local tracking data as retained records and avoid storing sensitive feed selections on shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/landercortazarromero/korta-blogwatcher) <br>
- [blogwatcher GitHub repository](https://github.com/Hyaxia/blogwatcher) <br>
- [blogwatcher Go module](https://pkg.go.dev/github.com/Hyaxia/blogwatcher/cmd/blogwatcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation and use of the blogwatcher CLI; the CLI may contact configured blog or feed URLs and keep local article tracking state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
