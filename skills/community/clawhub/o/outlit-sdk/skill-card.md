## Description: <br>
Use when integrating Outlit tracking into web, server, native, or desktop apps; adding SDK event tracking, identity, consent, activation, billing, visitor tracking, customerId attribution, or troubleshooting @outlit/browser, @outlit/node, or the Rust outlit crate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-paz](https://clawhub.ai/user/leo-paz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add or troubleshoot Outlit tracking across browser, server, native, and desktop applications, including identity, consent, event tracking, activation, billing, and customer attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics tracking can create visitor storage and collect product or website activity before consent and privacy requirements are settled. <br>
Mitigation: Confirm consent, privacy notice, and data-minimization requirements before enabling automatic tracking; use autoTrack false when consent is uncertain. <br>
Risk: Custom tracking events may send PII, secrets, or unnecessary form data to analytics if event properties are copied without review. <br>
Mitigation: Review event properties before instrumentation and avoid sending PII, secrets, or unnecessary form data. <br>


## Reference(s): <br>
- [Outlit Skill on ClawHub](https://clawhub.ai/leo-paz/skills/outlit-sdk) <br>
- [Outlit tracking quickstart](https://docs.outlit.ai/tracking/quickstart) <br>
- [How Outlit tracking works](https://docs.outlit.ai/tracking/how-it-works) <br>
- [Customer context graph](https://docs.outlit.ai/concepts/customer-context-graph) <br>
- [Identity resolution](https://docs.outlit.ai/concepts/identity-resolution) <br>
- [Outlit browser SDK](https://docs.outlit.ai/tracking/browser/npm) <br>
- [Outlit Node.js SDK](https://docs.outlit.ai/tracking/server/nodejs) <br>
- [Outlit Rust and Tauri SDK](https://docs.outlit.ai/tracking/server/rust) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SDK setup steps, environment variable names, event tracking examples, identity and consent recommendations, and troubleshooting checks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
