## Description: <br>
xAI (x.ai). Use this skill for any xAI request, including reading, creating, and updating data through the OOMOL `x_ai` connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate xAI through an OOMOL-connected account, inspect live connector schemas, and run chat completion or model metadata actions with the `oo` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs credentialed OOMOL connector actions for a connected xAI account, including a write action that may create chat completions or consume account credits. <br>
Mitigation: Inspect the live action schema before constructing payloads, confirm write payloads and expected effects with the user before execution, and use the skill only with an intended connected OOMOL/xAI account. <br>
Risk: First-time setup and recovery steps may require authentication, connection repair, or billing actions outside the normal read-only flow. <br>
Mitigation: Run setup commands only after an auth, connection, or billing error indicates they are needed, and verify the account and target connection before retrying. <br>


## Reference(s): <br>
- [xAI homepage](https://x.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-x-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses from connector runs are JSON objects containing data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
