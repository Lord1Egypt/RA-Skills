## Description: <br>
Onkos helps agents manage long-form fiction projects by retrieving story context, tracking facts and hooks, checking continuity, and updating project memory across chapters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallroya](https://clawhub.ai/user/smallroya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and agents use Onkos to plan, write, revise, and audit long-form fiction while keeping character state, facts, foreshadowing, summaries, and narrative continuity available across chapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read caller-supplied local files and import their contents into project memory. <br>
Mitigation: Review import paths and setting files before use, and avoid pointing the skill at sensitive files. <br>
Risk: The skill can delete, clear, update, or rewrite local novel-project data. <br>
Mitigation: Keep backups and require explicit confirmation before destructive or replacement actions. <br>
Risk: The skill can download an optional semantic-search model asset. <br>
Mitigation: Require explicit confirmation before model downloads and verify the intended source. <br>


## Reference(s): <br>
- [Onkos ClawHub release page](https://clawhub.ai/smallroya/onkos) <br>
- [Command reference](references/command_reference.md) <br>
- [Creation guide](references/creation_guide.md) <br>
- [Agent roles](references/agent_roles.md) <br>
- [Command index](references/command_index.md) <br>
- [Settings format](references/settings_format.md) <br>
- [Workflows](references/workflows.md) <br>
- [text2vec-base-chinese model](https://huggingface.co/shibing624/text2vec-base-chinese) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local project memory, chapter summaries, facts, hooks, character profiles, settings imports, and optional semantic-search model assets.] <br>

## Skill Version(s): <br>
1.6.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
