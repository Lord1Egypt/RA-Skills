## Description:

Provides real-time US stock quotes and financial data using the Finnhub API and Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyfrog-21k](https://clawhub.ai/user/keyfrog-21k)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to retrieve current US stock quote data from Finnhub when financial market context is needed in an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the unpinned finnhub-python package.

Mitigation: Pin finnhub-python to a reviewed version and install it in a virtual environment before use.

Risk: The skill requires a Finnhub API key and outbound network access.

Mitigation: Run it with only the required Finnhub API key available in the environment and avoid exposing broader secrets.

## Reference(s):

- [Finnhub](https://finnhub.io)
- [ClawHub skill page](https://clawhub.ai/keyfrog-21k/skills/openclaw-finnhub)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text quote output with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11+, the finnhub-python package, a Finnhub API key in the finnhub_api_key environment variable, and network access to Finnhub.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
