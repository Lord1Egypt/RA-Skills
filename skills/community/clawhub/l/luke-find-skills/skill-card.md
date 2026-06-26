## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banalit](https://clawhub.ai/user/banalit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find relevant installable skills, compare search results, and install a selected skill when they want to extend an agent's capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer broad requests toward persistent third-party skill installs while skipping install confirmations. <br>
Mitigation: Inspect the target skill's publisher and repository first, and avoid global installs with skipped confirmations unless the persistent user-level change is intentional. <br>
Risk: Search results may lead users to install skills that are not owned or reviewed by NVIDIA. <br>
Mitigation: Present the publisher, source link, and install command for user review before installing a selected skill. <br>


## Reference(s): <br>
- [Skills Registry](https://skills.sh/) <br>
- [Luke Find Skills on ClawHub](https://clawhub.ai/banalit/luke-find-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend search and install commands for the Skills CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
