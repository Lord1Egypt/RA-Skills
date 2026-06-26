## Description: <br>
Reports current AI model details including model name, provider, API endpoint, and session status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viratkumar123](https://clawhub.ai/user/viratkumar123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect the active OpenClaw model, provider, session status, token usage, cost, and runtime configuration during debugging or multi-model workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface model, provider, endpoint/key-source, token/cost, session, and runtime details in chat output. <br>
Mitigation: Invoke it only when those details are needed, prefer explicit prompts such as "model-info status", and avoid sharing the output publicly. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/viratkumar123/model-info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status summary with model, provider, API key source, session, token, cost, and runtime fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive runtime, endpoint, key-source, token, cost, and session details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
