## Description: <br>
梅花易数起卦，根据上卦、下卦数字查六十四卦，给出卦名、动爻及详解链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaobo1992](https://clawhub.ai/user/xiaobo1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to calculate an I Ching hexagram from upper and lower trigram numbers, then receive the hexagram name, moving line, a detail link, and brief Chinese interpretive guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python helper when invoked. <br>
Mitigation: Review the bundled script before deployment and run it only in the normal agent execution sandbox. <br>
Risk: The output may include external zhouyi.cc links for further reading. <br>
Mitigation: Inspect links before opening them and avoid entering sensitive information on third-party sites. <br>
Risk: Divination-style guidance can be misleading if treated as professional advice. <br>
Mitigation: Use the interpretation for reflection or entertainment only, not for legal, medical, financial, safety, or other high-stakes decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaobo1992/gua-helper) <br>
- [八卦对照表](references/bagua.md) <br>
- [十二时辰与时序对照表](references/shichen.md) <br>
- [六十四卦速查表](assets/64gua_table.md) <br>
- [卦意链接来源](references/guas.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style Chinese text with calculated hexagram fields and a reference URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Python helper during invocation; no artifact evidence of package installation, persistence, or data transmission.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
