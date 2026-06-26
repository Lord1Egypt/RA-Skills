## Description: <br>
Nexus helps an agent guide users through logging, querying, updating, and managing workout, meal, weight, and fitness-friend data with the Nexus CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiluazen](https://clawhub.ai/user/kiluazen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to install and operate the Nexus fitness CLI for explicit workout, meal, body-weight, history, update, authentication, and friend-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide use of a cloud-backed CLI that stores personal fitness, nutrition, and body-weight data. <br>
Mitigation: Review the Nexus privacy policy and OAuth prompts before use, and avoid logging sensitive details that are not needed. <br>
Risk: Friend-history features may expose another person's personal fitness data. <br>
Mitigation: Use friend data only with appropriate consent and limit requests to the user's intended fitness workflow. <br>
Risk: Installing the CLI runs third-party package code on the user's machine. <br>
Mitigation: Review the package source and release details before installation in sensitive environments. <br>


## Reference(s): <br>
- [Nexus ClawHub page](https://clawhub.ai/kiluazen/nexus-fitness) <br>
- [Nexus website](https://kushalsm.com/nexus) <br>
- [Nexus privacy policy](https://kushalsm.com/nexus/privacy-policy) <br>
- [Nexus terms of service](https://kushalsm.com/nexus/terms-of-service) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include OAuth authentication steps and user-provided fitness entry data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
