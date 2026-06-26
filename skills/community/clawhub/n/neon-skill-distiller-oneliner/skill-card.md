## Description: <br>
Skill compression reminder in 100 tokens: trigger, action, and result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to compress skill markdown into a minimal reminder that preserves the trigger, action, and result needed by an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aggressive compression can omit useful instructions or weaken the original skill behavior. <br>
Mitigation: Review the compressed output against the original skill before replacing it, especially protected patterns and expected behavior. <br>
Risk: LLM-estimated functionality scores can be approximate or misleading. <br>
Mitigation: Treat scores as review aids rather than validation results and test the compressed skill on representative tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/neon-skill-distiller-oneliner) <br>
- [Project homepage](https://github.com/live-neon/skills/tree/main/skill-distiller/oneliner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with a compressed skill, approximate functionality score, token reduction stats, and kept or removed section list.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Functionality scores are LLM-estimated and should be reviewed before replacing an original skill.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
