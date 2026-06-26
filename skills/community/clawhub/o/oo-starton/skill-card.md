## Description: <br>
Starton connector skill for reading, creating, updating, and deleting Starton data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Starton IPFS pins from an agent through the OOMOL oo CLI, including listing pins, reading pin details, creating JSON pins, pinning existing CIDs, and deleting pins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates through an OOMOL-brokered Starton connection and may use sensitive account credentials without exposing raw tokens to the agent. <br>
Mitigation: Install only when the user trusts OOMOL to broker the Starton connection and is comfortable allowing the agent to manage Starton IPFS pins through the oo CLI. <br>
Risk: Pin deletion can remove Starton data. <br>
Mitigation: Confirm the exact pin target and obtain explicit user approval before running destructive deletion actions. <br>
Risk: The pin_existing_file action creates a pin even though the artifact does not tag it as a write action. <br>
Mitigation: Ask for confirmation before running pin_existing_file, matching the security guidance for state-changing actions. <br>


## Reference(s): <br>
- [Starton homepage](https://starton.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action payload construction and may return oo CLI JSON responses when actions run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
