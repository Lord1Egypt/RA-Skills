## Description: <br>
Trades crypto hourly Up/Down markets on Polymarket when sub-interval consensus disagrees with the hourly price, using conviction-based sizing for BTC, ETH, and SOL opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to discover Polymarket crypto Up/Down market bundles, compare five-minute interval consensus against hourly markets, and run paper or explicitly enabled live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running with --live can place real Polymarket trades and expose the user to financial loss. <br>
Mitigation: Start in paper mode, keep position limits conservative, and enable --live only after reviewing the strategy and configuration. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Use a least-privileged Simmer API key, keep it out of logs and shared files, and rotate it if exposed. <br>
Risk: The advertised minimum-volume safeguard may not be reliable without verification or a fix. <br>
Mitigation: Verify the volume filter behavior before relying on it for live trading, or keep live trading disabled until the safeguard is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-bundle-crypto-hourly-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with Python code and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading and only places live Polymarket trades when run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence; artifact metadata also contains 1.0.0 frontmatter and 0.0.2 clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
