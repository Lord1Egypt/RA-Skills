## Description: <br>
Complete Miro Web SDK reference for building web plugins and desktop applications. Covers setup, core APIs (boards, shapes, text, items, selections, events), authentication, real-time collaboration, examples in TypeScript/JavaScript, best practices, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigbubbaagent-bot](https://clawhub.ai/user/bigbubbaagent-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill as a compact Miro Web SDK reference when building, configuring, testing, and troubleshooting Miro web plugins or desktop app integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copy-paste examples may be used as production plugin code without privacy or safety review. <br>
Mitigation: Treat the skill as reference documentation, test copied examples in a Miro Developer team, and review privacy and safety behavior before production use. <br>
Risk: Examples may request broader Miro scopes than a specific plugin needs. <br>
Mitigation: Request only the scopes required for the plugin workflow and verify permission errors during development testing. <br>
Risk: Logging user data or raw stack traces can expose sensitive information. <br>
Mitigation: Avoid logging PII or raw stack traces and keep secrets out of frontend environment variables. <br>
Risk: Board export or delete actions can change or remove user content. <br>
Mitigation: Add explicit user confirmation before export or delete operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bigbubbaagent-bot/miro-sdk) <br>
- [Miro developer documentation](https://developers.miro.com/docs) <br>
- [Miro API reference](https://developers.miro.com/reference) <br>
- [Setup and installation reference](references/setup-installation.md) <br>
- [Core APIs reference](references/core-apis.md) <br>
- [Authentication reference](references/authentication.md) <br>
- [Examples reference](references/examples.md) <br>
- [Best practices reference](references/best-practices.md) <br>
- [Error handling reference](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, JavaScript, JSON, shell, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference output; examples require review before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
