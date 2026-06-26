## Description: <br>
Integrates Merso PNPL payments into games or digital goods platforms with guidance for API setup, webhooks, payment flows, Node.js configuration, database records, troubleshooting, and commercial context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreadterror](https://clawhub.ai/user/dreadterror) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and commercial teams use this skill to add Merso installment payments to games, apps, and digital goods platforms, or to understand the technical and partner context for a Merso integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook handling can accept unsigned payment events. <br>
Mitigation: Require valid webhook authentication or verify each payment event server-side before granting or revoking items. <br>
Risk: The Merso API key is a sensitive credential required by the integration. <br>
Mitigation: Use development credentials first and protect MERSO_API_KEY in the deployment secret store. <br>
Risk: Commercial guidance says to omit fee discussion from pitch materials. <br>
Mitigation: Include fees and other material tradeoffs in decision-making documents and partner reviews. <br>


## Reference(s): <br>
- [Merso API Reference & Integration Guide](artifact/references/api.md) <br>
- [Merso Commercial Context, Case Studies & Partner Info](artifact/references/commercial.md) <br>
- [Merso production API](https://api2.merso.io) <br>
- [Merso development API](https://api2.dev.merso.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, API examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require MERSO_GAME_ID, MERSO_API_KEY, and MERSO_ENV for implementation guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
