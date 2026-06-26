## Description: <br>
Distills OpenClaw memory, session logs, and generated reports into evidence-backed knowledge points and knowledge leads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to review workspace-native memory, session, daily-note, and report materials, then produce a dated Markdown distillation of durable knowledge and follow-up leads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input memory, session, and report files may contain sensitive personal, business, or project information. <br>
Mitigation: Choose input and output directories deliberately, and review the generated Markdown before sharing, committing, or publishing it. <br>
Risk: Weak or one-off observations could be promoted into durable knowledge without enough support. <br>
Mitigation: Require a short basis for each knowledge point and keep partial signals in the leads section until they have stronger evidence. <br>
Risk: The helper script writes dated Markdown drafts to the selected output directory. <br>
Mitigation: Use an explicit output directory for each run and inspect the draft before treating it as retained knowledge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/knowledge-distillation) <br>
- [Output templates](artifact/references/output-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Dated Markdown file with structured sections for input summary, new knowledge points, knowledge leads, and round conclusions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script creates a dated draft file and leaves evidence-backed completion to the agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
