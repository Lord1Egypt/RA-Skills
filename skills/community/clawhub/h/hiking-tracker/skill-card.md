## Description: <br>
Hiking Tracker helps record hiking routes, analyze elevation, provide safety reminders, and surface weather alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to record hikes, inspect elevation changes, request safety reminders, and prepare weather-aware hiking summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather, trail safety, and emergency information may be incomplete, stale, or non-authoritative. <br>
Mitigation: Verify weather, trail conditions, safety notices, and emergency guidance with authoritative local sources before acting. <br>
Risk: The artifact metadata declares a curl binary requirement without a matching active implementation in the skill files. <br>
Mitigation: Review requested binaries during installation and allow network-capable tools only for expected, user-approved hiking assistant workflows. <br>


## Reference(s): <br>
- [Hiking Tracker ClawHub Release](https://clawhub.ai/kaising-openclaw1/hiking-tracker) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is instruction-only and may refer to hiking route, elevation, safety, weather, and statistics workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
