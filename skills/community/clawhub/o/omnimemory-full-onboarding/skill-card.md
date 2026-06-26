## Description: <br>
OmniMemory Full Onboarding helps an agent register or use an OmniMemory SaaS account, create API keys, install and configure the OpenClaw OmniMemory overlay plugin, repair setup mistakes, and run a memory smoke test. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pt-vu](https://clawhub.ai/user/pt-vu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external OpenClaw users use this skill to complete OmniMemory onboarding, install the OmniMemory overlay plugin, configure persistent memory settings, and verify the setup with a recall smoke test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles passwords, OTPs, access tokens, first-party API keys, and external LLM API keys. <br>
Mitigation: Use a unique password, prefer revocable API keys, avoid exposing full secrets in conversation logs, and verify that summaries mask sensitive values. <br>
Risk: The skill installs a third-party OpenClaw plugin and configures it to use a remote OmniMemory service. <br>
Mitigation: Install only if you trust the OmniMemory service and the @omni-pt plugin publisher, and review each installation or configuration command before execution. <br>
Risk: The skill can enable automatic remote memory recall and capture. <br>
Mitigation: Keep autoRecall and autoCapture disabled until the user understands what data may be stored and retrieved, then enable them only for appropriate sessions. <br>
Risk: The repair flow can mutate persistent OpenClaw configuration. <br>
Mitigation: Back up existing OmniMemory configuration before repair commands and confirm that corrected values are written under the documented .config paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pt-vu/omnimemory-full-onboarding) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [OmniMemory website](https://www.omnimemory.ai/zh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline API steps and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes masked secret summaries, setup status, warning notes, and final verification results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
