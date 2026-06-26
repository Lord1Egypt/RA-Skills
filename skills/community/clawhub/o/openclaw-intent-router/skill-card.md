## Description: <br>
Intelligently routes natural language user intents to the best matching registered agent skill using keyword and semantic matching with confidence scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building multi-agent systems, chatbots, API gateways, voice assistants, or workflow automation use this skill to route natural language requests to registered handlers with confidence scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed artifact documents an external npm package and GitHub repository that are not bundled in the artifact. <br>
Mitigation: Verify the package and repository before installation, prefer pinned versions, and run dependency checks such as npm audit after installing. <br>
Risk: Routed handlers may perform irreversible actions after an intent is matched. <br>
Mitigation: Require explicit user confirmation before any handler sends messages, modifies accounts or data, publishes content, spends money, or performs other irreversible actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ZhenStaff/openclaw-intent-router) <br>
- [npm package](https://www.npmjs.com/package/openclaw-intent-router) <br>
- [GitHub repository](https://github.com/ZhenRobotics/openclaw-intent-router) <br>
- [Quick Start](https://github.com/ZhenRobotics/openclaw-intent-router/blob/main/QUICKSTART.md) <br>
- [Examples](https://github.com/ZhenRobotics/openclaw-intent-router/tree/main/examples) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local installation, skill registration, routing, CLI usage, and confidence-threshold configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
