## Description:

Graceful rate limit handling with Ollama fallback. Notifies on rate limits, offers local model switch with confirmation for code tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhardie](https://clawhub.ai/user/dhardie)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to keep OpenClaw agents responsive when cloud LLM providers hit rate limits, while surfacing model-routing changes and requiring confirmation before local-model code work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter which model handles agent work, including switching from a cloud model to local Ollama after rate-limit errors.

Mitigation: Review the active LLM mode with `/llm status`, keep strict model-routing requirements in deployment policy, and switch back with `/llm switch cloud` when cloud access is required.

Risk: The advertised confirmation gate for local code work is not reliably enforced.

Mitigation: Review local-model code changes before applying them and require explicit human approval for sensitive or production code tasks.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses, notifications, command replies, and LLM routing configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session state tracks cloud or local mode, last rate-limit error, and Ollama model selection.]

## Skill Version(s):

0.3.0 (source: ClawHub release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
