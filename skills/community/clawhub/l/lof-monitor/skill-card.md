## Description: <br>
Monitors A-share LOF fund premium and discount gaps above a configured threshold to identify potential arbitrage signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kafroc](https://clawhub.ai/user/kafroc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to install and run a Python monitor that compares A-share LOF fund market prices with net asset values and reports funds whose premium or discount exceeds the configured threshold. The output is informational market monitoring data, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependencies are not fully pinned, and beautifulsoup4 is imported by the script but not listed in requirements.txt. <br>
Mitigation: Pin dependencies in a lockfile before deployment and add beautifulsoup4 explicitly to the installation requirements. <br>
Risk: The script contacts third-party financial-data sites and may produce stale, incomplete, or inaccurate market signals. <br>
Mitigation: Treat the output as informational monitoring data, verify results against authoritative market sources, and do not treat generated signals as financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kafroc/lof-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command snippets and a generated UTF-8 text output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes LOFMonitor_output.txt after querying third-party financial-data sources.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
