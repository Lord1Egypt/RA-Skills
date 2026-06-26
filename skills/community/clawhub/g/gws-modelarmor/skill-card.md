## Description: <br>
Google Model Armor: Filter user-generated content for safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to inspect Google Model Armor commands and prepare CLI calls for filtering prompts, responses, and templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the gws CLI and shared generated gws skills for authentication and security behavior. <br>
Mitigation: Install only if the gws CLI and generated shared skills are trusted, and review their security rules before use. <br>
Risk: Model Armor processing may involve prompts, responses, or other user-generated content that could contain sensitive or regulated data. <br>
Mitigation: Use least-privileged Google credentials and send secrets or regulated data only when policy allows Google Model Armor processing. <br>
Risk: Template creation or changes can alter filtering behavior. <br>
Mitigation: Confirm intended parameters and review proposed template changes before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-modelarmor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and generated shared gws skills for authentication, global flags, and security rules.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
