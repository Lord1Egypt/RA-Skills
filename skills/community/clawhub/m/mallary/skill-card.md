## Description: <br>
Mallary gives AI agents a unified interface for posting, scheduling, uploading media, checking analytics, managing profiles, webhooks, and settings across major social platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sammydigits](https://clawhub.ai/user/sammydigits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, CI jobs, and AI agents use this skill to automate Mallary social publishing workflows, including media uploads, post creation and scheduling, analytics checks, dashboard profile targeting, webhooks, settings, and platform management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can publish, schedule, delete, disconnect platforms, manage settings, and configure webhooks for real Mallary-connected social accounts. <br>
Mitigation: Install only when that live authority is intended, use a least-privilege or test API key, and verify the target profile and platform before posting, deleting, disconnecting, or changing settings. <br>
Risk: Credential examples and authenticated CLI use can expose MALLARY_API_KEY if the key is printed or stored persistently in shell profiles. <br>
Mitigation: Do not print the API key, avoid storing it permanently in shell profiles, and prefer scoped environment injection such as CI secrets or temporary shell sessions. <br>
Risk: Local media paths and webhook URLs are sent outside the machine through Mallary workflows. <br>
Mitigation: Treat local media paths and webhook URLs as externally shared data and review them before upload or webhook creation. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sammydigits/skills/mallary) <br>
- [Mallary website](https://mallary.ai/) <br>
- [Mallary CLI npm package](https://www.npmjs.com/package/@mallary/cli) <br>
- [Mallary API documentation](https://docs.mallary.ai/) <br>
- [Create endpoint platform options](https://docs.mallary.ai/api-reference/endpoint/create#body-platform-options) <br>
- [Platform-specific media rules](https://docs.mallary.ai/api-reference/endpoint/create#platform-specific-media-rules) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MALLARY_API_KEY for authenticated Mallary CLI commands.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
