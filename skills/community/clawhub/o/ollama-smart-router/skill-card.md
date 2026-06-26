## Description: <br>
Routes user prompts between local, remote, and specialist Ollama models using task-complexity classification, system profiling, health checks, caching, conversation context, and optional SearXNG search augmentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncatbot](https://clawhub.ai/user/simoncatbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route prompts to a cost- or capability-appropriate Ollama model while keeping simple work local where possible. It supports mixed local and remote Ollama deployments with model availability checks, streaming responses, fallbacks, and optional web-search context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be sent to a configured remote Ollama server or to a SearXNG endpoint when web search is enabled. <br>
Mitigation: Use only trusted endpoints, force local-only routing when needed, and disable search unless external web lookups are intended. <br>
Risk: Prompt fragments, routing decisions, classifications, and conversation history may be stored locally in logs or SQLite cache files. <br>
Mitigation: Avoid entering secrets, restrict access to log and cache paths, review retention settings, and clear stored history when handling sensitive work. <br>
Risk: The authoritative security review flags under-disclosed prompt persistence and optional web-search behavior. <br>
Mitigation: Review the skill before installing and disclose data routing, persistence, and search behavior to users before deployment. <br>


## Reference(s): <br>
- [Classifier prompt reference](references/classifier-prompt.txt) <br>
- [ClawHub skill page](https://clawhub.ai/simoncatbot/ollama-smart-router) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON routing metadata followed by streamed plain text or Markdown response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include routing status, optional web-search context, and streamed model response chunks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and __init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
