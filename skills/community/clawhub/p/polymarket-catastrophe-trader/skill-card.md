## Description: <br>
Trades Polymarket prediction markets on hurricane seasons, earthquake probabilities, wildfire forecasts, and extreme weather records using catastrophe-market bias correction and seasonal data quality timing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and run a Polymarket catastrophe-market trading workflow that discovers relevant markets, sizes positions, and places paper or explicitly enabled live orders through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real financial orders. <br>
Mitigation: Start in paper mode, avoid --live unless real trades are intended, and keep conservative position limits. <br>
Risk: SIMMER_API_KEY grants trading authority. <br>
Mitigation: Use the least-privileged key available and protect it as a sensitive credential. <br>
Risk: Catastrophe markets may be thin or volatile. <br>
Mitigation: Use the configured max position, max spread, minimum volume, and max open position controls before considering live execution. <br>


## Reference(s): <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Plain text logs, configuration values, and Simmer SDK trading requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require the --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
