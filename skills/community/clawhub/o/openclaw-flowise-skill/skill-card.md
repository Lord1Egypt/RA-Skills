## Description: <br>
Interact with Flowise AI workflows via REST API to list chatflows, inspect flows, send predictions, and manage conversation sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianmu](https://clawhub.ai/user/tianmu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to connect to configured Flowise servers, select chatflows, send user messages, and return Flowise responses with optional session context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts, files, API keys, and action-style script or device parameters to a configured Flowise server. <br>
Mitigation: Install only when the Flowise server and configured flows are trusted, keep API keys in protected secret storage, and require explicit user approval before uploads or script/device actions. <br>
Risk: Incorrect or overly broad flow mappings could route user requests to an unintended Flowise workflow. <br>
Mitigation: Review TOOLS.md flow mappings carefully and verify the selected flow before sending sensitive prompts, files, or custom variables. <br>


## Reference(s): <br>
- [Flowise skill page](https://clawhub.ai/tianmu/openclaw-flowise-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Flowise API responses, curl commands, configuration guidance, and error summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
