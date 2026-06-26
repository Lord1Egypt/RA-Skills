## Description: <br>
Needle helps an agent operate Needle collections through the OOMOL oo CLI, including listing, inspecting, creating, adding URL-backed files, checking stats, and searching retrieved content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to work with Needle collections from an OOMOL-connected account. It supports read workflows such as listing, inspecting, statistics lookup, and search, plus write workflows for creating collections and adding URL-backed files for indexing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Needle collections or add URL-backed files for indexing, which changes content available in the connected Needle account. <br>
Mitigation: Confirm the exact write payload and expected account effect before approving create or add-file actions. <br>
Risk: The skill requires access to a connected OOMOL/Needle account. <br>
Mitigation: Install and use it only when the agent is expected to operate that connected account. <br>


## Reference(s): <br>
- [Needle homepage](https://needle.app) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-needle) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that inspect live connector schemas and run Needle actions through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
