## Description: <br>
Hivulse蜂巢 AI helps developers generate standardized technical documents from a selected software project directory through the Hivulse cloud service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mojo-bo-coder](https://clawhub.ai/user/mojo-bo-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to upload a project directory and request generated requirements, design, testing, or security assessment documents. It supports OpenClaw and command-line workflows that require a Hivulse API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload broad project contents to Hivulse cloud. <br>
Mitigation: Use a cleaned copy of the project and remove environment files, credentials, customer data, private keys, and proprietary files before running. <br>
Risk: The skill stores or reads API keys from OpenClaw settings and local configuration. <br>
Mitigation: Treat OpenClaw API-key settings and ~/.hivulseai/config.json as sensitive, and prefer an isolated environment with pinned dependencies for sensitive work. <br>
Risk: The selected directory and document type determine what data is uploaded and what document is generated. <br>
Mitigation: Verify the exact directory and requested document type before upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mojo-bo-coder/hivulse-openclaw-skill) <br>
- [Publisher profile](https://clawhub.ai/user/mojo-bo-coder) <br>
- [Hivulse website](https://www.hivulse.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text technical documents with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Hivulse API key plus a selected project directory, document type, and optional task name.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
