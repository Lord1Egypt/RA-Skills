## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penglovemeng](https://clawhub.ai/user/penglovemeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover installable skills for a requested task, compare relevant options, and install selected skills with the Skills CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend broad activation or global installation of discovered skills. <br>
Mitigation: Review each skill name, source, and install scope before installing; avoid skipping CLI confirmation unless that is intentional. <br>
Risk: Search results or suggested skills may not match the user's needs or trust expectations. <br>
Mitigation: Compare the returned skill description, repository or source, and available links before presenting or installing a candidate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/penglovemeng/peng-find-skills) <br>
- [Skills directory](https://skills.sh/) <br>
- [Example skill listing](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include install commands that use global installation or skip CLI confirmation when the user chooses to proceed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
