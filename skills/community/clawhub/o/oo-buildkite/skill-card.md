## Description: <br>
Buildkite helps agents read and manage Buildkite organizations, pipelines, and builds through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CI operators use this skill to let an agent inspect Buildkite account, organization, pipeline, and build data, and to perform approved build operations such as create, cancel, and rebuild. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform state-changing Buildkite operations such as creating, canceling, or rebuilding builds. <br>
Mitigation: Confirm the exact organization, pipeline, build number, payload, and intended effect with the user before running state-changing actions. <br>
Risk: The skill depends on an OOMOL-connected Buildkite account and can use sensitive credentials through that connection. <br>
Mitigation: Install and use it only when the user intends to let an agent operate Buildkite through OOMOL, and have the user approve oo CLI installation, sign-in, and connection steps. <br>


## Reference(s): <br>
- [ClawHub Buildkite skill page](https://clawhub.ai/oomol/oo-buildkite) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Buildkite homepage](https://buildkite.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Buildkite connector actions through the oo CLI when the user has connected an OOMOL account.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
