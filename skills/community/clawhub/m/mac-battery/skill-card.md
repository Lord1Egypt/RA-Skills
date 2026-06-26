## Description: <br>
Checks a Mac laptop's battery percentage, charging state, and time remaining using the local pmset command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airbai](https://clawhub.ai/user/airbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mac users can ask an agent for laptop battery status, and the agent can run the standard local pmset command to report percentage, charging state, and remaining time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is only useful on macOS systems where pmset is available. <br>
Mitigation: Use it for Mac laptops only; on other systems, say battery status is unavailable instead of trying unrelated commands. <br>
Risk: The skill asks the agent to run a local shell command. <br>
Mitigation: Run only the documented read-only pmset battery-status command and do not change power settings. <br>


## Reference(s): <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/airbai/mac-battery) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Friendly text response with battery status values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses macOS pmset battery output; no files are created.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
