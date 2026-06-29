## Description: <br>
LLM Gateway routes agent prompts to GoCreative AI completion endpoints across cheap, pro, and ultra model tiers with x402 pay-per-call billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colinhughes2121](https://clawhub.ai/user/colinhughes2121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request AI text completions and route prompts across cost and quality tiers without managing separate model-provider accounts or API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to a third-party GoCreative service and may be exposed in URL logs because the prompt is encoded in the request path. <br>
Mitigation: Do not include secrets, credentials, regulated data, confidential documents, or private customer information unless GoCreative documents acceptable retention and logging practices. <br>
Risk: The skill uses x402 pay-per-call endpoints, so agent use can incur per-request USDC charges. <br>
Mitigation: Review the selected tier and pricing before use, and configure wallet or spending controls appropriate for the agent workflow. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/colinhughes2121/gocreative-llm) <br>
- [GoCreative AI API](https://api.gocreativeai.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, text] <br>
**Output Format:** [Markdown guidance with HTTP GET endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts are URL-encoded in request paths; x402 payment may be required before the completion is returned.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
