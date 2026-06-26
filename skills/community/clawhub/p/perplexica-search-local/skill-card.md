## Description: <br>
AI-powered search using your local Perplexica instance. Runs deep research with web search and LLM reasoning, then returns answers with cited sources while keeping search state in Perplexica. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eplt](https://clawhub.ai/user/eplt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to query a local Perplexica instance for AI-powered web, academic, or discussion search and receive cited answers in an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, optional conversation history, and custom instructions are sent to the local Perplexica instance, and Perplexica may forward that data to its configured search or LLM providers. <br>
Mitigation: Use this skill only with a trusted local Perplexica deployment, review its configured providers, and avoid sending sensitive data unless those providers are approved for it. <br>
Risk: The skill depends on a reachable local Perplexica service with configured chat and embedding models, so missing or misconfigured local services can cause failed or incomplete searches. <br>
Mitigation: Confirm Perplexica is running locally, verify model provider setup before use, and use the documented timeout and mode options for long-running searches. <br>


## Reference(s): <br>
- [Perplexica Search on ClawHub](https://clawhub.ai/eplt/perplexica-search-local) <br>
- [Perplexica](https://github.com/ItzCrazyKns/Perplexica) <br>
- [OpenClaw](https://open-claw.bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Human-readable answer with cited sources, or JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports quiet output, source selection, optimization mode, custom instructions, conversation history, and configurable local Perplexica URL.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
