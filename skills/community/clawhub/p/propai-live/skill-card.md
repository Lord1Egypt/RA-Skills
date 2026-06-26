## Description: <br>
PropAI Live is an AI-powered realtor automation suite that bundles OpenClaw core, PropAI Sync, Social Flow, lead-processing skills, license checks, and approval-focused CLI and UI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalgojha](https://clawhub.ai/user/vishalgojha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Real estate teams and developers use this skill to plan and run PropAI Live workflows for lead follow-up, WhatsApp and Meta operations, social posting, and AI assistance while checking license state and requiring confirmation for write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes agents toward real WhatsApp, Meta, lead-storage, and spending workflows through dependencies and a CLI that are not included or scoped in the submitted artifact. <br>
Mitigation: Install only from a trusted publisher, verify the propai-live CLI and dependency skills before use, and require explicit confirmation before live messages, social posts, lead writes, or spending actions. <br>
Risk: License activation and validation depend on a configured remote license API and a locally cached license state file. <br>
Mitigation: Use a trusted license API URL, protect the local license state file, and run the license guard before write or entitlement-gated workflows. <br>


## Reference(s): <br>
- [PropAI Live ClawHub page](https://clawhub.ai/vishalgojha/propai-live) <br>
- [OpenClaw docs](https://openclaw.ai) <br>
- [License API contract](references/license-api-contract.md) <br>
- [License API starter template](assets/license-api/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON status output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state assumptions, mark risk levels, and request confirmation before write actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
