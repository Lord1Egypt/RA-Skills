## Description: <br>
Teaches AI agents how to learn better by enforcing deep correction, transfer learning, and proactive pattern recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fahrulalwan](https://clawhub.ai/user/fahrulalwan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Metaskill to add structured reflection to agent workflows: deep correction after errors, analogy checks before complex tasks, and capture of successful patterns after completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs may capture task details, error descriptions, or sensitive notes. <br>
Mitigation: Review the logging workflow before enabling it and avoid putting secrets or confidential content into correction or success notes. <br>
Risk: Configured LLM providers may receive task descriptions, error details, and excerpts from prior learnings. <br>
Mitigation: Use the local Ollama configuration for sensitive work, and configure API-backed providers only for content approved for external processing. <br>
Risk: The Gemini provider should not be used for sensitive work until the API-key-in-URL implementation is corrected. <br>
Mitigation: Prefer Anthropic, OpenAI, or local Ollama provider settings, or disable Gemini in the configuration. <br>
Risk: Automation can write into a self-improving-agent learning directory when present. <br>
Mitigation: Review AGENTS.md wiring and the selected learning-log path before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fahrulalwan/metaskill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Terminal text and Markdown learning logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured LLM providers for extraction, transfer checks, and evaluation, or fall back to manual and heuristic modes.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
