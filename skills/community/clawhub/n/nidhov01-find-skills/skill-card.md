## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find installable skills for specialized workflows, evaluate search results, and install selected skills with the Skills CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The example install command uses global installation and skips CLI confirmation. <br>
Mitigation: Review the target skill and publisher first; remove -y for interactive confirmation and omit -g when persistent user-level installation is not desired. <br>
Risk: Search results may point to third-party skills with different trust, maintenance, or security profiles. <br>
Mitigation: Inspect the skill page, publisher profile, and release evidence before installing or using a discovered skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nidhov01/nidhov01-find-skills) <br>
- [Skills directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and skill links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include install commands that invoke npx skills.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
