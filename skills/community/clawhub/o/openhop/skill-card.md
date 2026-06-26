## Description: <br>
Turn agent explanations into local animated flow diagrams, described in YAML and played back one hop at a time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naorsabag](https://clawhub.ai/user/naorsabag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use OpenHop to turn code paths, service architectures, product workflows, pipelines, state machines, and user journeys into local animated flow diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or run the OpenHop CLI through npx and start local services on ports 8787 and 8788. <br>
Mitigation: Confirm the user is comfortable with local CLI execution and localhost services before running setup or serve commands. <br>
Risk: Generated flow content is stored locally by OpenHop. <br>
Mitigation: Avoid diagramming sensitive workflows when local storage is not acceptable, or provide a plain-text explanation instead. <br>


## Reference(s): <br>
- [OpenHop homepage](https://github.com/naorsabag/openhop) <br>
- [OpenHop ClawHub listing](https://clawhub.ai/naorsabag/openhop) <br>
- [Provenance](unavailable: No server-resolved GitHub import provenance is stored for this version.) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [YAML flow specifications, shell commands, JSON command responses, and local flow URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local OpenHop flow content and returns a localhost URL for the rendered diagram.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
