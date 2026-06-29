## Description: <br>
Anchor Browser (anchorbrowser.io) helps an agent read Anchor Browser project billing and metadata, inspect live connector schemas, and start browser sessions through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Anchor Browser through OOMOL's connector, including checking billing details, retrieving project metadata, and starting browser sessions with schema-validated payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start an Anchor Browser session, which changes Anchor Browser state. <br>
Mitigation: Confirm the exact payload and effect with the user before running actions tagged as write. <br>
Risk: First-time setup may execute remote installer scripts for the oo CLI. <br>
Mitigation: Run installer commands only when the CLI is missing and only after the user trusts OOMOL and the installer source. <br>
Risk: Connector writes depend on the live action schema and the user's connected OOMOL account. <br>
Mitigation: Inspect the current connector schema before execution and review schema-derived payloads before writes. <br>


## Reference(s): <br>
- [Anchor Browser homepage](https://anchorbrowser.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return connector response data, execution IDs, browser CDP URLs, and live-view URLs from Anchor Browser actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
