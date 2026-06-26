## Description: <br>
Quantitative research and data tools for AI agents with 670+ PREF MCP capabilities and self-service agent key onboarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morluto](https://clawhub.ai/user/morluto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to register and configure an agent-owned PREF MCP key, connect a remote MCP endpoint, and verify authenticated access for quantitative research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PREF agent keys are sensitive credentials that could be exposed through terminal history, logs, prompts, or shared configuration. <br>
Mitigation: Store the key as a secret, avoid echoing or logging it, and reference it through an environment variable or protected credentials file. <br>
Risk: The remote PREF MCP service receives research queries and tool arguments sent by the agent. <br>
Mitigation: Install only if the operator trusts pref.trade for those queries, and review MCP capabilities before sensitive or high-impact use. <br>
Risk: A stale or incomplete MCP client configuration can silently use anonymous quota instead of the intended agent key. <br>
Mitigation: Verify access with preference_account_status and confirm the MCP client sends an Authorization: Bearer header. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/morluto/pref) <br>
- [PREF homepage](https://pref.trade) <br>
- [PREF MCP endpoint](https://pref.trade/mcp) <br>
- [PREF agent registration](https://pref.trade/v1/agents/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, YAML, JSON, and text examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces onboarding and verification guidance for a remote MCP service; it does not include local executable code.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
