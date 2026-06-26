## Description: <br>
Claid AI lets agents operate the Claid AI image-editing connector through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to edit public images with Claid AI through OOMOL-managed connector actions, including synchronous edits and asynchronous task submission and polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connected service credentials and can run Claid AI write actions through the OOMOL connector. <br>
Mitigation: Confirm the exact action payload and expected effect with the user before running write actions, and rely on OOMOL-managed credentials rather than handling raw API tokens. <br>
Risk: Connector action schemas may change over time, which can make a previously valid payload incorrect. <br>
Mitigation: Inspect the live action schema before constructing or submitting each connector payload. <br>
Risk: Authentication, connection, or billing failures can interrupt task execution. <br>
Mitigation: Use the documented recovery steps only after a command fails for the matching reason. <br>


## Reference(s): <br>
- [Claid AI homepage](https://claid.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-claid-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
