## Description: <br>
私人《论语》——你就是孔子，agent是你的学生。捕捉你的灵感金句、哲理妙语、生活洞察、幽默色话，自动整理成属于你自己的语录集。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyxin-del](https://clawhub.ai/user/joeyxin-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual Hermes users use this skill to capture memorable personal quotes, organize them by chapter, tag, and type, search the archive, receive a daily quote, and export a compiled Markdown edition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores selected conversation snippets and surrounding context in a local personal quote archive, which may include sensitive personal or work material if users save it. <br>
Mitigation: Install only when local storage under ~/.hermes/lunyu/ is acceptable, avoid saving secrets or confidential content, review entries before export or notification use, and delete or edit accidental captures with the documented commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joeyxin-del/lunyu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Conversational text with local JSON archive entries and optional Markdown export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and manages a personal quote archive under ~/.hermes/lunyu/ when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
