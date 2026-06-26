## Description: <br>
OpenClaw PII Anonymizer scrubs sensitive text such as names, email addresses, file paths, and IP addresses through a configured Ollama model before content is sent to external tools or models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solmas](https://clawhub.ai/user/solmas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to anonymize workspace, memory, and tool-call text before sending it to external LLMs or services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive text is sent to the configured Ollama endpoint for anonymization. <br>
Mitigation: Use localhost, host-only Ollama, or another explicitly trusted endpoint and review OLLAMA_URL before integrating the skill. <br>
Risk: The anonymized output is not a guaranteed privacy boundary for all datasets. <br>
Mitigation: Test the skill against representative sensitive data before relying on the output in external tool calls or model requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/solmas/openclaw-pii-anonymizer-latest) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured Ollama endpoint and limits input to 10000 characters.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
