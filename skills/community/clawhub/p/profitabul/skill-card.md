## Description: <br>
Real-time futures market intelligence, GEX/options flow analysis, trading signals, paper trading, backtesting, and live execution via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeurge](https://clawhub.ai/user/codeurge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-focused agent users use this skill to retrieve market context, GEX-derived levels, historical analysis, backtests, and paper or live trade operations through a Profitabul MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable real futures trades through an agent, including live order, position, and cancellation operations. <br>
Mitigation: Use paper trading or read-only workflows by default and require explicit human approval before any live order, position change, or cancellation. <br>
Risk: The skill depends on a private Profitabul API key. <br>
Mitigation: Keep PROFITABUL_API_KEY private, scope it to the least privilege available, and avoid exposing it in prompts, logs, or shared configuration. <br>
Risk: Trading signals and market analysis can be incorrect, incomplete, delayed, or financially risky. <br>
Mitigation: Treat outputs as decision support, review them independently, and apply the user's own risk limits before acting. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/codeurge/profitabul) <br>
- [Profitabul homepage](https://profitabul.ai) <br>
- [Profitabul API documentation](https://profitabul.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PROFITABUL_API_KEY and may return market data, signal summaries, backtest results, paper trade state, or live execution responses from the MCP service.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
