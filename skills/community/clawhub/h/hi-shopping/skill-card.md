## Description: <br>
Helps OpenClaw agents search products, confirm shipping details, and place immediate or scheduled purchases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atomicservice](https://clawhub.ai/user/atomicservice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to search shopping results, select goods, confirm delivery information, and automate immediate or scheduled purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place and schedule purchases using stored credentials and delivery addresses. <br>
Mitigation: Install only when the publisher is trusted, protect the configuration file, and confirm purchase authority before enabling the skill. <br>
Risk: Bundled or persistent configuration can expose cloud auth codes and shipping address data. <br>
Mitigation: Replace or remove bundled config values before use, keep credentials scoped, and avoid sharing the configured skill directory. <br>
Risk: Scheduled purchases may spend money later when the user is not present. <br>
Mitigation: Schedule purchases only when the user can review or cancel the task and accepts delayed execution. <br>
Risk: The skill depends on a remote shopping service for search and purchase execution. <br>
Mitigation: Verify the configured remote service before use and review command outputs before completing purchases. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/atomicservice/hi-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown product lists, JSON command results, shell command guidance, and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local session cache and confirmation files while completing shopping flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
