## Description: <br>
世界-角色有机验证：确认每个核心角色被世界所塑造，每个世界规则驱动某个角色的困境。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Story developers, writing agents, and narrative workflow maintainers use this skill after world design and character arc work to verify that characters are shaped by the world and that world rules create character dilemmas before Pilot Forge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads worldbuilding, character, and theme files from CLAW_WORKSPACE. <br>
Mitigation: Run it only in the intended project workspace and confirm those planning files are appropriate for agent review. <br>
Risk: The PASS, CONDITIONAL, or FAIL result could be mistaken for an automatic decision to keep or discard creative work. <br>
Mitigation: Treat the report as editorial guidance and review the findings before changing project direction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangliujiao-tal/planner-world-character-sync) <br>
- [Publisher profile](https://clawhub.ai/user/huangliujiao-tal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with validation tables and PASS, CONDITIONAL, or FAIL status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces world-character-sync.md in CLAW_WORKSPACE/03-世界 when executed by an agent with workspace write access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
