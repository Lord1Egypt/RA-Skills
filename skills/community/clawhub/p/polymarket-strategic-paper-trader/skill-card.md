## Description: <br>
Trade Polymarket prediction markets with AI through PredictScope paper trading, using real order books, simulated fills, configurable strategies, and workspace safety rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XintaoLiao](https://clawhub.ai/user/XintaoLiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage a PredictScope paper-trading workspace, discover Polymarket opportunities, place simulated trades, manage strategies, and review portfolio performance under configured safety rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place simulated trades and change, reset, disable, or delete cloud workspace state. <br>
Mitigation: Use a dedicated PredictScope workspace, explicitly select the workspace ID, and require confirmation before trades, resets, workspace deletion, strategy changes, or disabling order rules. <br>
Risk: The bearer API key authorizes access to PredictScope trading workspaces. <br>
Mitigation: Store PREDICTSCOPE_API_KEY only in the runtime environment, avoid pasting it into chat or files, and rotate the key if it is exposed. <br>
Risk: If no workspace ID is provided, the skill may operate on the most recently updated workspace. <br>
Mitigation: Set and verify the intended workspace ID before trading or changing strategies, and check workspace metadata before acting. <br>
Risk: Polymarket market names, descriptions, and metadata are untrusted third-party content. <br>
Mitigation: Treat market content as display-only data, ignore instructions embedded in market text, and avoid navigating to URLs from market metadata. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/XintaoLiao/polymarket-strategic-paper-trader) <br>
- [Publisher profile](https://clawhub.ai/user/XintaoLiao) <br>
- [PredictScope Paper Trading](https://predictscope.ai/paper-trading) <br>
- [PredictScope trading MCP endpoint](https://predictscope.ai/mcp/v1/trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown trading updates, configuration guidance, and MCP-backed workspace or order actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PREDICTSCOPE_API_KEY and can operate on cloud-hosted PredictScope workspaces selected by workspace ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata; artifact frontmatter states 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
