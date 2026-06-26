## Description: <br>
Guided SOP for setting up and using OpenMAIC from OpenClaw, including cloning, startup-mode selection, provider-key configuration, service startup, and classroom generation from requirements or PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyuc](https://clawhub.ai/user/wyuc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and educators use this skill to guide OpenMAIC setup, hosted or local startup, provider-key configuration, health checks, and classroom generation from requirements or PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted mode and classroom generation may send requirements, parsed PDF content, and an access code to the OpenMAIC hosted service. <br>
Mitigation: Use hosted mode only when comfortable sending that content to open.maic.chat, keep access codes in local config rather than chat, and use local mode for sensitive materials. <br>
Risk: Local setup can run clone, install, startup, and API request commands that affect the user's machine or contact external services. <br>
Mitigation: Review the OpenMAIC repository before approving commands, confirm each state-changing step, and inspect server-side provider configuration before generation. <br>
Risk: Provider keys and model configuration errors can cause generation failures or accidental use of an unintended provider. <br>
Mitigation: Store provider keys in local OpenMAIC configuration files, include provider prefixes in model IDs, and correct server-side config rather than using request-time overrides. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyuc/openmaic) <br>
- [Clone Or Reuse Existing Repo](references/clone.md) <br>
- [Generate Flow](references/generate-flow.md) <br>
- [Hosted Mode](references/hosted-mode.md) <br>
- [Provider Keys](references/provider-keys.md) <br>
- [Startup Modes](references/startup-modes.md) <br>
- [OpenMAIC hosted service](https://open.maic.chat) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, API request details, and generated classroom links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before state-changing local actions and before reading local PDFs.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
