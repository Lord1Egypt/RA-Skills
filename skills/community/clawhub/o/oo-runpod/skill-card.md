## Description: <br>
Runpod (runpod.io). Use this skill for ANY Runpod request - reading, creating, updating, and deleting data. Whenever a task involves Runpod, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Runpod pods through an OOMOL-connected account, including reads, lifecycle operations, and explicitly approved destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run powerful Runpod actions, including write and destructive pod operations. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before write actions, and require explicit approval before destructive actions. <br>
Risk: The skill requires a connected OOMOL account and sensitive service credentials. <br>
Mitigation: Use OOMOL server-side credential injection and avoid exposing raw Runpod tokens in prompts, logs, or command payloads. <br>


## Reference(s): <br>
- [Runpod homepage](https://www.runpod.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before Runpod action execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
