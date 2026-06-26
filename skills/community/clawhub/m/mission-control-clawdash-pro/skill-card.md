## Description: <br>
Create or update detailed, publish-ready instructions for wiring Mission Control (ClawDash Pro) prebuilt Next.js UI to Open Cloud after purchase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[petercsipkay](https://clawhub.ai/user/petercsipkay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External customers and developers use this skill to create publish-ready setup instructions for connecting a purchased ClawDash Pro Next.js dashboard to Open Cloud while preserving the existing UI design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated setup instructions may be applied in an untrusted or incorrect project directory. <br>
Mitigation: Run npm commands only inside the trusted purchased Mission Control project and review generated steps before execution. <br>
Risk: Credential handling mistakes could expose Open Cloud API keys or workspace identifiers. <br>
Mitigation: Keep .env.local out of source control and use least-privilege Open Cloud API keys. <br>
Risk: Connected dashboard data may expose token usage, document state, or other workspace information. <br>
Mitigation: Verify access controls before exposing token usage, document data, or operational dashboard views. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/petercsipkay/mission-control-clawdash-pro) <br>
- [ClawDash Pro](https://clawdash.pro) <br>
- [Mission Control Publish Instruction Template](references/publish-instruction-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline text and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One Markdown instruction file by default; variants only when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
