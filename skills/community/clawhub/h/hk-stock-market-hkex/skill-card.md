## Description:

Get HKEX (Hong Kong Stock Exchange) market data via FinanceAgent on OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve HKEX stock quote data for one or more stock symbols through FinanceAgent on OneKey Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing commands can expose the OneKey Gateway API key through verbose curl output, shell history, logs, CI output, or support transcripts.

Mitigation: Keep DEEPNLP_ONEKEY_ROUTER_ACCESS out of logs and transcripts, avoid curl -v for credentialed requests, and use environment handling appropriate for secrets.

Risk: The skill relies on an unpinned executable npm package from the OneKey Gateway provider.

Mitigation: Install only if the provider and npm package publisher are trusted, and prefer a pinned, project-local package install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/hk-stock-market-hkex)
- [DeepNLP OneKey Agent Router endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON request/response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS and accepts a symbol_list array of HKEX stock code strings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
