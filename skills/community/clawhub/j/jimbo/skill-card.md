## Description: <br>
Jimbo helps with financial analysis, budget-conscious decisions, value investing, and RSI-based investment signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tycooncoder](https://clawhub.ai/user/tycooncoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this agent for financial analysis, budgeting tradeoffs, and investment screening based on value-investing and RSI mean-reversion heuristics. Reviewers should also account for bundled workspace, memory, automation, and ClawStreet paper-trading behavior before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release bundles broad workspace, memory, heartbeat, automation, and unrelated skill behavior beyond the finance-assistant description. <br>
Mitigation: Review the full package before installing and remove unrelated workspace, skill, and memory files when only the finance assistant is needed. <br>
Risk: Heartbeat-style automation and ClawStreet behaviors can trigger recurring background checks, API calls, public feed activity, or paper-trading actions. <br>
Mitigation: Tighten heartbeat triggers and require explicit confirmation before registration, public/API actions, or recurring trading workflows. <br>
Risk: The bundled workspace can access or persist personal context through memory files. <br>
Mitigation: Audit memory files before deployment and avoid loading personal memory in shared or untrusted contexts. <br>
Risk: Trading API keys or bot credentials may be needed for ClawStreet behavior. <br>
Mitigation: Store credentials only in a secure credential store and never commit, log, or expose API keys in prompts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tycooncoder/jimbo) <br>
- [ClawStreet API](https://www.clawstreet.io/api) <br>
- [ClawStreet indicators reference](https://www.clawstreet.io/skills/clawstreet/INDICATORS.md) <br>
- [ClawStreet strategies reference](https://www.clawstreet.io/skills/clawstreet/STRATEGIES.md) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown text with optional shell commands, API request examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce financial analysis and paper-trading actions; not financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
