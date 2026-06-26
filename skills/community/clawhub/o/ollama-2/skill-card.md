## Description: <br>
Ollama helps agents call a local or configured Ollama API endpoint for text generation with selectable host, model, and prompt settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayflying](https://clawhub.ai/user/ayflying) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send prompts to an Ollama model through the Ollama generate API, test connectivity, and customize host and model selection for local or controlled inference workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be sent to the default non-local Ollama host if the environment is not configured. <br>
Mitigation: Confirm that http://100.66.1.2:11434 is the intended server, or set OLLAMA_HOST to a trusted local or controlled endpoint before use. <br>
Risk: Sensitive prompts could be exposed to a remote or unauthenticated Ollama endpoint. <br>
Mitigation: Avoid sending sensitive prompts unless the configured Ollama host is trusted and access-controlled. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, Python code, and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The query helper returns generated text or error text from the configured Ollama endpoint.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
