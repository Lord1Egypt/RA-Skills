## Description: <br>
Initializes hersona persona on first use of a profile and assists in maintaining the applied speech style if deviation is detected during conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiro-0x](https://clawhub.ai/user/shiro-0x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users who want a ClawHub profile to automatically apply and maintain a configured Hersona persona use this skill to initialize persona settings, provide manual reapplication commands, and assist when speech style drifts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause the profile to consistently use the configured Hersona persona and Japanese speech style when that behavior is not desired. <br>
Mitigation: Review the suggested SOUL.md default command before adding it, and omit or remove it when neutral behavior or only explicit persona changes are preferred. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shiro-0x/skills/hersona-initializer) <br>
- [Server-resolved GitHub source](https://github.com/shiro-0x/hersona/tree/main/skills/hersona-initializer) <br>
- [Hersona project homepage](https://github.com/shiro-0x/hersona) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, commands, configuration] <br>
**Output Format:** [Markdown with slash-command examples and a profile configuration snippet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code or external access found in the security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
