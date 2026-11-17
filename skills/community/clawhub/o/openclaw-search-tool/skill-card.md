## Description:

Searches the web using LLMs via OpenRouter for current web data, API docs, market research, news, fact-checking, and questions that benefit from live internet access and reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronn](https://clawhub.ai/user/aaronn)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw agents use this skill to perform live web research, documentation lookups, market and news research, and fact-checking with cited sources through OpenRouter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an external Cargo-installed CLI that uses an OpenRouter API key.

Mitigation: Install only from a reviewed or pinned version and protect the API key with normal secret-handling practices.

Risk: Research queries may be built from untrusted text, creating command-construction risk when invoked through a shell.

Mitigation: Pass queries through safe argument handling or use --stdin instead of interpolating untrusted text into shell commands.

Risk: OpenRouter usage can incur per-query costs.

Mitigation: Use an API key with spending limits and choose reasoning effort levels appropriate to the task.

## Reference(s):

- [Openclaw Search Tool Homepage](https://github.com/aaronn/openclaw-search-tool)
- [OpenRouter API Keys](https://openrouter.ai/keys)
- [ClawHub Skill Page](https://clawhub.ai/aaronn/skills/openclaw-search-tool)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response text with citations on stdout; progress, reasoning status, and token usage on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the research-tool binary and OPENROUTER_API_KEY; supports effort, model, system prompt, stdin, max token, and timeout options.]

## Skill Version(s):

0.1.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
