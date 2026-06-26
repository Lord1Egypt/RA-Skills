## Description: <br>
Libu Premarket generates an A-share pre-market stock screening map using capital-flow signals, financial filters, and technical indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ygbeyond](https://clawhub.ai/user/ygbeyond) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare a pre-market A-share market report, including global market context, sector flow analysis, selected stock candidates, and trading guidance for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad local file and environment access and reads payment and market-data credentials from environment variables. <br>
Mitigation: Install only from a trusted publisher, run in an environment where those credentials may be read by the skill, and avoid exposing unrelated secrets. <br>
Risk: The skill may load Python code from a separate local tushare-finance skill directory if that path exists. <br>
Mitigation: Review any local tushare-finance files before running this skill, or run it in a clean environment without that local skill path. <br>
Risk: The output includes stock-screening and trading guidance that may be incomplete, stale, or unsuitable for a user's risk profile. <br>
Mitigation: Treat generated reports as data references only, verify market data independently, and require human investment review before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ygbeyond/libu-premarket) <br>
- [Publisher profile](https://clawhub.ai/user/ygbeyond) <br>
- [Tushare Pro](https://tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Console text plus pre_market_data.json for agent-readable market report data; documentation also describes Markdown report content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python dependencies and payment credential setup; optionally uses TUSHARE_TOKEN for fresher market data.] <br>

## Skill Version(s): <br>
14.0.6 (source: server release, manifest.json, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
