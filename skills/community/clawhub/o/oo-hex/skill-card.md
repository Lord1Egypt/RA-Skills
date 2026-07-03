## Description: <br>
Hex (hex.tech). Use this skill for Hex requests involving reading, creating, and updating data through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to operate Hex projects from an agent through an OOMOL-connected account, including project discovery, run inspection, triggering published project runs, and canceling in-progress runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on OOMOL to broker access to the user's Hex account. <br>
Mitigation: Install and use the skill only when the user trusts OOMOL with that account connection. <br>
Risk: CLI installation commands download and execute installer scripts. <br>
Mitigation: Review any oo CLI installation command before running it. <br>
Risk: Triggering a Hex project run may consume credits or affect downstream data depending on the project. <br>
Mitigation: Confirm the target project and payload with the user before running project actions that can change state or incur cost. <br>


## Reference(s): <br>
- [Hex homepage](https://hex.tech) <br>
- [oo CLI repository](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-hex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, text, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to fetch live connector schemas before building action payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
