## Description: <br>
Crypto research via Grok model's real-time X/Twitter knowledge; forwards the user's query as-is to a Grok API for token narrative, story, sentiment, and crypto Twitter research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arespollo](https://clawhub.ai/user/arespollo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to send a user's crypto research question to a Grok API and return narrative, story, sentiment, or crypto Twitter context about a token or project. It is not intended for price analysis, on-chain data analysis, or trading execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's full research message verbatim to an external Grok API endpoint. <br>
Mitigation: Avoid including secrets, private wallet details, nonpublic project information, or trading strategy in prompts. <br>
Risk: The activation wording is broad enough that it may be invoked for general research requests. <br>
Mitigation: Invoke it explicitly for crypto narrative or sentiment research and review whether the request should be sent to the external service. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text response on stdout with status and errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires A9_GROK_API_KEY and supports a selectable Grok model; requests are sent to the disclosed external API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
