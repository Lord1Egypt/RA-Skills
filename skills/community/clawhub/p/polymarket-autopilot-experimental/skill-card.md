## Description: <br>
Analyzes public Polymarket markets, simulates paper trades, tracks LLM costs, and produces concise Italian reports for controlled experimental use. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[mauonga](https://clawhub.ai/user/mauonga) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, market analysts, and non-expert users use this skill to run controlled, read-only analysis of public Polymarket markets, simulate paper-trading decisions, and compare simulated outcomes against LLM costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes prediction markets and could be mistaken for real trading guidance. <br>
Mitigation: Use it only for read-only public market analysis and paper trading; do not add wallet access, authenticated trading access, real-money execution, or private data. <br>
Risk: Budget limits are behavioral instructions rather than an enforceable sandbox. <br>
Mitigation: Set external OpenAI and Anthropic spending limits and monitor token usage outside the skill. <br>
Risk: Automated market filtering and LLM ranking can be incomplete or misleading. <br>
Mitigation: Treat reports as experimental analysis, require human review before decisions, and keep the configured cadence and low-budget constraints. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/mauonga/polymarket-autopilot-experimental) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Italian Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes observed market count, simulated percentage and EUR result, detailed LLM costs, simulated net result, cautious agent commentary, and a final two-line summary.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
