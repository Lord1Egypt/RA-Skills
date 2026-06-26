## Description: <br>
Interact with Hevy fitness app data through the hevy CLI to view, create, and update workouts, routines, exercise templates, and routine folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sajal2692](https://clawhub.ai/user/sajal2692) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect and manage Hevy fitness account data through documented hevy CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HEVY_API_KEY grants access to the user's Hevy account. <br>
Mitigation: Keep HEVY_API_KEY in protected environment configuration and do not paste or log it. <br>
Risk: The skill can propose commands that create or update workouts, routines, exercises, or folders. <br>
Mitigation: Review write commands and their JSON payloads before execution. <br>


## Reference(s): <br>
- [Hevy CLI Command Reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read, create, or update Hevy account data; raw JSON output is available with the -j flag.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
