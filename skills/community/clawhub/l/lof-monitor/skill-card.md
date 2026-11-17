## Description:

Monitors A-share LOF fund premium or discount levels above a 10% threshold and outputs potential arbitrage opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kafroc](https://clawhub.ai/user/kafroc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents can use this skill to run an A-share LOF fund monitor, identify funds with large premium or discount gaps, and report the resulting arbitrage candidates. It is most relevant for finance-oriented workflows that need scripted market-data checks and concise text output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can fail or drift over time because the artifact uses dependency ranges and its install command omits the requirements-file flag.

Mitigation: Use a virtual environment, install with pip install -r requirements.txt, and pin or lock dependency versions before production use.

Risk: The script contacts public financial data sources and overwrites LOFMonitor_output.txt in the current working directory.

Mitigation: Run it from a controlled working directory and review network access and output-file handling before automating it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text fund monitoring results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes matching LOF fund opportunities to LOFMonitor_output.txt after retrieving public financial data.]

## Skill Version(s):

1.0.1 (source: release evidence and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
