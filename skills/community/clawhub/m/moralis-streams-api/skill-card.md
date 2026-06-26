## Description: <br>
Real-time blockchain event monitoring with webhooks for setting up, managing, and troubleshooting Moralis Streams across EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novnski](https://clawhub.ai/user/novnski) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure Moralis Streams, create or update webhook streams, add and remove monitored addresses, replay webhook history, and troubleshoot stream delivery behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Moralis API key to create, change, delete, and replay webhook streams. <br>
Mitigation: Require explicit user confirmation before deleting streams, replaying webhooks, changing webhook URLs, enabling all-address monitoring, or updating project settings. <br>
Risk: Moralis API keys, stream secrets, and webhook signatures may be exposed if pasted into chat or committed to source control. <br>
Mitigation: Keep MORALIS_API_KEY in an environment variable or ignored .env file, and mask secretKey and signature values in shared output. <br>
Risk: Webhook testing with untrusted or public endpoints can expose real event data. <br>
Mitigation: Use trusted HTTPS webhook endpoints and avoid public request-bin URLs for real stream data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/novnski/moralis-streams-api) <br>
- [Moralis Documentation](https://docs.moralis.com) <br>
- [Moralis Onchain Skills Repository](https://github.com/MoralisWeb3/onchain-skills) <br>
- [Common Pitfalls Reference](references/CommonPitfalls.md) <br>
- [Stream Configuration Reference](references/StreamConfiguration.md) <br>
- [Webhook Security](references/WebhookSecurity.md) <br>
- [Delivery Guarantees](references/DeliveryGuarantees.md) <br>
- [Error Handling, Retries, and Stream Lifecycle](references/ErrorHandling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and MORALIS_API_KEY for authenticated Moralis Streams API calls.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
