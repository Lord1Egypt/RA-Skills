## Description: <br>
Hire is an interactive hiring wizard that guides role design for a new AI team member, generates agent identity files, and can set up performance reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larsderidder](https://clawhub.ai/user/larsderidder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use Hire to define a new AI team member through a guided interview, select an appropriate model, generate agent files, and update team configuration after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent agent files, modify OpenClaw gateway configuration, expand subagent permissions, link shared user memory, and optionally create cron jobs. <br>
Mitigation: Review generated files, shared-context links, allowlist changes, cron schedules, and the exact configuration patch before allowing changes to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/larsderidder/hire) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Conversational Markdown with generated agent files, shell commands, and configuration patches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent agent directories, shared-context links, gateway configuration patches, and optional cron schedules.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
