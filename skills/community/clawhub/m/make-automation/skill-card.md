## Description: <br>
Manage Make.com organizations, users, teams, scenarios, and billing. Configure organization settings, manage team members, retrieve usage analytics, and access pricing information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a Make account through ClawLink and manage Make organizations, teams, users, usage analytics, billing information, and supported Make API reference data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates against a connected Make account and may access organization, user, billing, and usage data. <br>
Mitigation: Use the ClawLink-hosted OAuth flow, verify the active Make connection before calls, and avoid collecting API keys or tokens in chat. <br>
Risk: Write operations can change organizations or trigger user-facing actions such as password reset emails. <br>
Mitigation: Preview unfamiliar or write actions, confirm the target resource and intended effect with the user, and execute only after confirmation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/make-automation) <br>
- [Make API Documentation](https://www.make.com/en/api-docs) <br>
- [Make Help Center](https://www.make.com/en/help) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=make-automation) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and ClawLink tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active Make account, ClawLink pairing, and explicit user confirmation for write or destructive operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
