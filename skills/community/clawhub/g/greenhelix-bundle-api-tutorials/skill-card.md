## Description: <br>
A bundle of 22 API-heavy tutorials for the GreenHelix A2A Commerce Gateway covering agent commerce, verification, incident response, migration, compliance, trading infrastructure, and security hardening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this bundle as tutorial guidance for building, securing, operating, and monetizing agent commerce workflows against the GreenHelix production API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundle requests powerful production-style credentials, including Stripe, signing, wallet, and GreenHelix API values, without explaining why each credential is needed. <br>
Mitigation: Review the relevant guide before use and provide only sandbox or tightly scoped test credentials until the credential purpose and handling requirements are verified. <br>
Risk: Credential values could be exposed through shared chats, logs, or broad agent context while following API tutorials. <br>
Mitigation: Keep secrets out of shared prompts and logs, scope them to the current task, and rotate any value that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mirni/greenhelix-bundle-api-tutorials) <br>
- [Publisher profile](https://clawhub.ai/user/mirni) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tutorials with API code examples and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GREENHELIX_API_KEY as the primary environment variable and may reference AGENT_SIGNING_KEY, STRIPE_API_KEY, and WALLET_ADDRESS.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
