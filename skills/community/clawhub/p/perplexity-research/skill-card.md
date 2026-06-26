## Description: <br>
Conduct deep research using Perplexity Agent API with web search, reasoning, and multi-model analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hushenglang](https://clawhub.ai/user/hushenglang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and AI agents use this skill to run current-information research, market analysis, trend analysis, investment research, and multi-model comparisons through the Perplexity Agent API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts, pasted context, conversation history, and optional location fields may be sent to Perplexity. <br>
Mitigation: Avoid sensitive or regulated data unless policy allows it, and review prompts before sending them to the API. <br>
Risk: The skill requires a Perplexity API key and can incur API usage costs. <br>
Mitigation: Use a dedicated, rotatable API key with spending controls and keep .env files out of source control. <br>
Risk: Copied examples may write local report files or run API calls in the user's environment. <br>
Mitigation: Review examples and generated commands before executing them or allowing file writes. <br>


## Reference(s): <br>
- [Perplexity API](https://www.perplexity.ai/api) <br>
- [ClawHub skill page](https://clawhub.ai/hushenglang/perplexity-research) <br>
- [README.md](README.md) <br>
- [examples.md](examples.md) <br>
- [reference.md](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; API client methods return JSON-like dictionaries or streamed text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-streaming calls include answer, token, cost, and model fields; streaming calls print text to the console.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
