## Description: <br>
Helps an agent publish Markdown articles to a local Hugo blog by generating front matter, creating tag and category mapping files, adding a summary marker, and preparing git publish commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blog maintainers use this skill to turn Markdown article content into Hugo post files, taxonomy mapping files, and reviewed git publishing steps for a local blog repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local memory or configuration files that may contain secrets or private notes. <br>
Mitigation: Require the agent to identify the exact files it plans to read and avoid broad memory-file access unless the files are known to be safe. <br>
Risk: The skill can stage, commit, and push Hugo blog changes with git without clear approval checkpoints. <br>
Mitigation: Require the agent to show the exact file changes and git commands first, then give separate explicit approval before any commit or push. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/hugo-blog-publisher-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML front matter examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Hugo content files and taxonomy _index.md files; git commit and push commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
