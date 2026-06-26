## Description: <br>
Seqera (seqera.io). Use this skill for ANY Seqera request - searching and reading data. Whenever a task involves Seqera, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Seqera through an OOMOL-connected account, including reading users, workspaces, pipelines, and workflow runs, and launching workflows when explicitly intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch Seqera workflows, which may change state or incur cost even though the action is not labeled as a write action in the skill text. <br>
Mitigation: Confirm the exact payload, workspace, pipeline, and cost impact with the user before running launch_workflow. <br>
Risk: The first-time setup instructions include remote installer commands. <br>
Mitigation: Review the CLI installer source or use OOMOL's documented installation path before running pipe-to-shell commands. <br>
Risk: The skill requires an OOMOL-connected Seqera account and therefore depends on sensitive credentials managed outside the skill. <br>
Mitigation: Install only when the publisher is trusted and the user intends to operate Seqera through the OOMOL oo CLI. <br>


## Reference(s): <br>
- [Seqera homepage](https://seqera.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL Seqera connection](https://console.oomol.com/app-connections?provider=seqera) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-seqera) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses may include JSON data and an execution ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
