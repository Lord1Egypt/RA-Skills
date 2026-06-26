## Description: <br>
Provides 24/7 real-time financial news updates from sources such as Jin10 through a Prana remote service, returning pass-through results for agent display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luokeer52](https://clawhub.ai/user/luokeer52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request current financial-news updates for monitoring market developments. The local package forwards the request to a Prana service and returns the service response without rewriting it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and Prana credentials to a remote Prana endpoint. <br>
Mitigation: Install only when the configured Prana endpoint is trusted, and use a dedicated API key for this skill. <br>
Risk: The thin client can store API credentials in config/api_key.txt as plaintext. <br>
Mitigation: Prefer environment-provided credentials or set PRANA_SKILL_SKIP_WRITE_API_KEY=1 to avoid writing fetched keys to disk; never commit config/api_key.txt. <br>
Risk: Remote responses are passed through without local rewriting or validation. <br>
Mitigation: Review returned market-news content before acting on it, especially for trading, investment, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luokeer52/market-beats) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill manifest](artifact/skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Pass-through JSON from the Prana agent-run or agent-result API; content may include market-news text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and Prana API credentials; long-running requests may be recovered by polling agent-result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
