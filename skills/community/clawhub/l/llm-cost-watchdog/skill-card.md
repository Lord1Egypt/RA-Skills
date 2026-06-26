## Description: <br>
Monitors real-time LLM API costs, detects runaway loops, enforces budgets, audits code risk, and reports usage across multiple providers and models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimaansari](https://clawhub.ai/user/nimaansari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to monitor LLM API spend, estimate costs before expensive work, detect unbounded agent loops, and enforce budget ceilings during agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local usage metadata and error logs may reveal model names, token counts, spend, timestamps, and related workflow metadata. <br>
Mitigation: Use a scoped CW_LOG_DIR with appropriate local access controls, and clear logs with the reset command when retention is not needed. <br>
Risk: Optional session-log readers and HTTP capture can broaden the monitoring scope beyond a single SDK wrapper. <br>
Mitigation: Enable these hooks only in processes where broad LLM response metadata capture is acceptable, and prefer SDK-specific wrappers when narrower coverage is sufficient. <br>
Risk: Token validation and live pricing features may contact provider services. <br>
Mitigation: Use non-sensitive validation samples, avoid sending secrets, and set offline or static-only modes when network lookups are not appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nimaansari/llm-cost-watchdog) <br>
- [Cost Watchdog Skill Definition](artifact/SKILL.md) <br>
- [Cost Watchdog README](artifact/README.md) <br>
- [Token Counting & Cost Calculation](artifact/references/calculators.md) <br>
- [Cost Optimization Strategies](artifact/references/optimization.md) <br>
- [Dangerous Cost Patterns & Safe Alternatives](artifact/references/patterns.md) <br>
- [API Pricing Reference](artifact/references/pricing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local JSONL usage, error, and cache files under the configured cost-watchdog log directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
