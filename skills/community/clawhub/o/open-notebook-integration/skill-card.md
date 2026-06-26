## Description: <br>
Integrates OpenClaw agents with a local open-notebook service for creating, saving, and querying thematic notebooks using local Ollama models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to connect agents to a local notebook service, save knowledge across sessions, create topic-specific notebooks, and query stored notes through the local API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local open-notebook checkout and Docker Compose setup, so running untrusted service files could expose the user to unsafe local execution. <br>
Mitigation: Use only a trusted open-notebook checkout and review the Docker Compose configuration before starting local containers. <br>
Risk: Notebook content is saved to a persistent local service and may include sensitive notes if the user stores them there. <br>
Mitigation: Avoid storing secrets, tokens, or sensitive personal data unless the user has reviewed how the local service stores and exposes notebook data. <br>
Risk: The skill sends content and queries to local HTTP API endpoints, so misconfigured or exposed services could make notebook data accessible outside the intended local workflow. <br>
Mitigation: Keep the open-notebook API bound to trusted local access and verify container status and endpoint configuration before use. <br>


## Reference(s): <br>
- [Open Notebook Skill on ClawHub](https://clawhub.ai/nantes/open-notebook-integration) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown documentation with PowerShell functions and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local open-notebook service, Docker, Ollama, notebook IDs, and local API endpoints configured by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata and artifact version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
