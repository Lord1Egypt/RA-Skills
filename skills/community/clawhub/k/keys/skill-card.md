## Description: <br>
Secure API key management with broker. Keys never exposed to agent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to make authenticated API requests through an OS keychain-backed broker without exposing API keys in agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broker gives agents authenticated access to sensitive provider APIs. <br>
Mitigation: Use restricted or read-only API keys where possible and require manual confirmation before mutating API calls. <br>
Risk: Verification or management commands can print stored secrets into an agent-visible terminal. <br>
Mitigation: Avoid running commands that display key values; guide users to OS keychain prompts and secret storage commands instead. <br>
Risk: The skill is flagged for review because its documentation and broker behavior can expose or use high-privilege credentials. <br>
Mitigation: Review carefully before installation and avoid high-privilege Stripe or GitHub tokens unless they are necessary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/keys) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Key Management Guide](artifact/manage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Broker calls return JSON responses from configured API services.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
