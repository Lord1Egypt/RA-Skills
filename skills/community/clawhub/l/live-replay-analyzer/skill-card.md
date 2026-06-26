## Description: <br>
Live Replay Analyzer generates detailed livestream replay and growth planning reports from client and session data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, livestream operators, and agents use this skill to turn livestream data, audience profile information, and session scripts into a structured replay analysis and growth plan. It can output an assembled analysis prompt or call a configured model API to save a timestamped Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw livestream or customer data may be sent to a configured external model provider. <br>
Mitigation: Use only an approved provider and endpoint, redact sensitive data before use, and use a dedicated limited API key. <br>
Risk: Client and session inputs are used to locate local files without clear path validation. <br>
Mitigation: Use trusted client and session names only, keep inputs inside the expected skill input directory, and add path validation before broad deployment. <br>
Risk: The release does not include server-resolved source provenance and the security guidance calls for pinned dependencies. <br>
Mitigation: Review the packaged files directly, pin runtime dependencies, and request a maintained source repository before production rollout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsbnb/live-replay-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/ahsbnb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Prompt text or Markdown report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires client and session identifiers, local input files, and an optional configured model API key for direct report generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
