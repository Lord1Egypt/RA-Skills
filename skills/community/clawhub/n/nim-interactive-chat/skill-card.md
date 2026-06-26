## Description: <br>
Generates interactive chat scripts for NVIDIA NIM-compatible models, including start and stop scripts, service readiness checks, and an OpenAI-compatible streaming chat client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romancestarrysky](https://clawhub.ai/user/romancestarrysky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create local launch, stop, and chat scripts for NVIDIA NIM-compatible Docker model services. It is suited for quickly starting a containerized model, waiting for readiness, and entering an interactive OpenAI-compatible chat session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated start script may remove an existing container when the same container name is reused. <br>
Mitigation: Review generated scripts before running them and choose a unique container name for each deployment. <br>
Risk: The Docker image source controls the model service that will run locally. <br>
Mitigation: Verify the Docker image source and tag before starting the container. <br>
Risk: Exiting the interactive chat can leave the model container running in the background. <br>
Mitigation: Use the generated stop script when the service is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romancestarrysky/nim-interactive-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands and generated shell/Python file descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces start and stop shell scripts plus a Python chat client for a named container and model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
