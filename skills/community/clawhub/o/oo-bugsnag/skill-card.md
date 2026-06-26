## Description: <br>
Bugsnag lets an agent search and read Bugsnag organizations, projects, errors, releases, and events through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and incident responders use this skill to query Bugsnag data from an OOMOL-connected account without handling raw Bugsnag tokens directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup instructions include a remote installer run directly in a shell. <br>
Mitigation: Review and trust the OOMOL install guide or use a verified package-manager path before running the installer. <br>
Risk: The skill requires account access and sensitive credentials through an OOMOL-connected Bugsnag account. <br>
Mitigation: Install only when the OOMOL publisher and connected account are trusted, and keep credential scope limited to the needed Bugsnag access. <br>


## Reference(s): <br>
- [Bugsnag skill page](https://clawhub.ai/oomol/oo-bugsnag) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Bugsnag homepage](https://www.bugsnag.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs Bugsnag connector actions through the oo CLI and can return JSON responses from Bugsnag.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
