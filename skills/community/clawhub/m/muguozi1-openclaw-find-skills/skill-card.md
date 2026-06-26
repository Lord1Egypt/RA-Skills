## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search for relevant installable skills, present options with install commands, and optionally install selected skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent global installation of third-party skills and includes a confirmation-skip flag. <br>
Mitigation: Review each suggested skill's publisher and source before installing, avoid confirmation skips, and prefer non-global installation unless persistence is intended. <br>
Risk: Skill-discovery results can lead an agent to recommend untrusted or unsuitable third-party packages. <br>
Mitigation: Treat search results as candidates, inspect the selected skill's source and permissions, and ask the user before running installation commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muguozi1/muguozi1-openclaw-find-skills) <br>
- [Skills browser](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose third-party skill installation commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
