## Description: <br>
Operates updown.io monitoring checks and node information through the OOMOL updown_io connector using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to inspect and manage updown.io monitoring checks, list monitoring nodes, and retrieve node IP addresses through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The first-time setup path can install the OOMOL oo CLI from a shell command. <br>
Mitigation: Install only from a trusted OOMOL source or verified install path before running connector actions. <br>
Risk: The skill can create, update, and delete updown.io monitoring checks. <br>
Mitigation: Confirm exact payloads and effects with the user before write actions, and require explicit approval before destructive actions. <br>
Risk: Connector requests depend on OOMOL CLI/service behavior and connected account credentials. <br>
Mitigation: Use the skill only when the user trusts OOMOL and has intentionally connected the updown.io account. <br>


## Reference(s): <br>
- [updown.io homepage](https://updown.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-updown-io) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to inspect live connector schemas before sending action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
