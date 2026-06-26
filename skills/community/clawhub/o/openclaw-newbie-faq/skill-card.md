## Description: <br>
Provides a beginner-oriented OpenClaw guide with large-model concepts, FAQ answers, command references, optimization tips, and a local web interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kunyashaw](https://clawhub.ai/user/kunyashaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to launch a local beginner guide for onboarding, troubleshooting, command lookup, and performance-tuning guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoking the skill can start a background local Node.js web server with unclear exposure and stop controls. <br>
Mitigation: Install only when a local FAQ server is intended, confirm the bind address and port 34567 availability, and stop the node process manually if needed. <br>
Risk: Broad trigger phrases such as help requests may accidentally launch the local guide server. <br>
Mitigation: Review trigger phrases before deployment and use explicit launch wording when interacting with the agent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kunyashaw/openclaw-newbie-faq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Local web guide and Markdown-style instructional content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts or references a local Node.js web server on port 34567 for the guide interface.] <br>

## Skill Version(s): <br>
1.0.44 (source: server release evidence and skill.json; SKILL.md and package.json list 1.0.43) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
