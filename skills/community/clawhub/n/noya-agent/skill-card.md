## Description: <br>
Noya Agent lets agents interact with the Noya AI agent for crypto trading, prediction markets, token analysis, portfolio checks, and DCA strategy workflows via curl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ali-hajeh](https://clawhub.ai/user/ali-hajeh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask Noya for crypto portfolio information, token and market analysis, swaps, bridges, transfers, DCA strategies, and prediction-market actions. It is intended for crypto and prediction-market workflows that require explicit user confirmation before high-impact actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support high-impact crypto trading, transfers, orders, bridges, and DCA actions through a remote agent. <br>
Mitigation: Review every transaction or market-action confirmation before approval and never auto-confirm interrupt prompts. <br>
Risk: The skill uses NOYA_API_KEY to authenticate to the remote Noya service. <br>
Mitigation: Use a short-lived or limited API key when possible, keep unrelated secrets out of prompts, and revoke the key when testing or use is complete. <br>
Risk: The security evidence notes an endpoint disclosure mismatch. <br>
Mitigation: Verify that NOYA_BASE_URL is unset or points to the intended Noya API host before use. <br>


## Reference(s): <br>
- [Noya Agent API Reference](reference.md) <br>
- [Noya Agent Website](https://agent.noya.ai) <br>
- [Noya API Base URL](https://safenet.one) <br>
- [ClawHub Skill Page](https://clawhub.ai/ali-hajeh/noya-agent) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/ali-hajeh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streams parsed Noya API responses, including messages, tool results, progress updates, errors, and interrupt prompts that require user input.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
