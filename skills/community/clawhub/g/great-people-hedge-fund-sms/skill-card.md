## Description: <br>
Coordinates multiple investor-persona and analysis agents to evaluate stocks, synthesize viewpoints, and produce investment-style signals with conviction levels. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investment researchers can use this skill to request ticker analysis, compare stocks, and receive synthesized buy, hold, or sell signals with risk and conviction commentary. Outputs should be treated as informational research rather than personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated investment signals, position sizes, and entry strategies may be incorrect, incomplete, or unsuitable for a user's circumstances. <br>
Mitigation: Treat outputs as informational research, independently verify market data and analysis, and consult qualified financial advice before making investment decisions. <br>
Risk: The skill may require sensitive LLM credentials and optional market-data network access. <br>
Mitigation: Install only in environments where credential handling and outbound data access are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smseow001/great-people-hedge-fund-sms) <br>
- [Publisher profile](https://clawhub.ai/user/smseow001) <br>
- [ai-hedge-fund inspiration project](https://github.com/virattt/ai-hedge-fund) <br>
- [Nanobot framework](https://github.com/HKUDS/nanobot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, guidance] <br>
**Output Format:** [Markdown-style investment report with signals, conviction scores, agent viewpoints, risk assessment, and key insights; README also describes optional JSON and table formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on LLM credentials and optional market-data network access; financial outputs require independent verification before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
