## Description: <br>
Meta Skill System is a Chinese-language meta-skill for domain evaluation, workflow restructuring, domain skill generation, and general task execution using a reusable three-axis methodology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, workflow designers, and agent operators use this skill to assess whether domains should exist, simplify complex workflows, generate domain-specific skill payloads, and execute methodology-heavy tasks with structured templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad prompt authority may steer agent behavior beyond a narrow user task. <br>
Mitigation: Install only when the broad meta-skill behavior is intentional, and narrow activation terms before routine use. <br>
Risk: The artifact instructs agents not to refuse skill-content changes. <br>
Mitigation: Remove or override the blanket non-refusal instruction and require normal user approval for edits to skills or prompts. <br>
Risk: Generated workflow or skill guidance could include shell/python execution or file edits. <br>
Mitigation: Require explicit approval and human review before executing commands or applying generated edits. <br>


## Reference(s): <br>
- [Meta Skill Catalog](references/meta-skill-catalog.md) <br>
- [Meta Skill Requirements](references/meta-skill-requirements.md) <br>
- [Meta Skill Exemplars](references/exemplars.md) <br>
- [Merged Meta Skill Prompt](references/meta-skill-system-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with generated skill or workflow content when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce task decompositions, domain evaluations, workflow plans, skill file drafts, and review checklists.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
