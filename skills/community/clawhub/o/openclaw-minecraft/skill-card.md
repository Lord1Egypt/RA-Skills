## Description: <br>
Control Minecraft bots through a Mineflayer controller API using JSON actions and cron-driven autonomy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ene5135](https://clawhub.ai/user/ene5135) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create and direct Mineflayer-based Minecraft bots, turning goals into JSON action batches and cron-driven autonomous loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autonomous Minecraft bot actions may continue every 30 seconds through cron. <br>
Mitigation: Enable the loop only when persistent autonomy is intended, and add clear start, stop, logging cleanup, and server-safety limits before use. <br>
Risk: Replacing the workspace root CRON_PROMPT.md can overwrite existing cron behavior. <br>
Mitigation: Merge or namespace the cron instructions instead of blindly replacing an existing CRON_PROMPT.md. <br>
Risk: The skill sends bot actions through an external controller endpoint. <br>
Mitigation: Verify that the controller endpoint is owned or trusted, and use scoped, revocable agent tokens. <br>


## Reference(s): <br>
- [OpenClaw Minecraft on ClawHub](https://clawhub.ai/ene5135/openclaw-minecraft) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Cron prompt](artifact/CRON_PROMPT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and JSON action payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces controller instructions for supported Minecraft bot actions and cron-loop behavior.] <br>

## Skill Version(s): <br>
0.1.26 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
