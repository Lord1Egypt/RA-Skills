## Description: <br>
Abyssale helps agents read, create, and update Abyssale data through the OOMOL oo CLI instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Abyssale from an agent session, including listing designs and projects, inspecting designs and formats, creating projects or dynamic image URLs, and generating banners from JSON element overrides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected Abyssale account and requires sensitive credential access. <br>
Mitigation: Use the existing OOMOL connection and avoid handling raw API tokens; run setup or reconnection only after an auth or connection error. <br>
Risk: Write actions can create Abyssale projects or dynamic image URLs. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged as write or destructive. <br>
Risk: Action inputs can drift from the expected schema or produce unintended banner outputs. <br>
Mitigation: Inspect the live connector schema before constructing payloads and review JSON overrides before execution. <br>


## Reference(s): <br>
- [Abyssale homepage](https://www.abyssale.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-abyssale) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include connector data and execution metadata when actions are run with --json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
