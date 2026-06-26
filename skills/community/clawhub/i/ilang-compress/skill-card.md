## Description: <br>
Compress natural language prompts into I-Lang — AI-native structured instructions. 40-65% token savings. Output is text notation only — review before passing to execution agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adsorgcn](https://clawhub.ai/user/adsorgcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert natural-language prompts into compact I-Lang notation, usually to reduce token usage while preserving the intended task semantics. The output should be reviewed before it is passed to agents or tools that may interpret compressed verbs as executable instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compressed I-Lang output may contain verbs and resource references that a downstream execution agent could interpret as real file, network, or cloud operations. <br>
Mitigation: Review compressed output before passing it to execution environments, and keep confirmation or dry-run controls enabled for agents that can act on the notation. <br>
Risk: Prompt compression can omit nuance or make intent harder for a human reviewer to inspect. <br>
Mitigation: Compare the compressed notation and its explanation against the source prompt before using it for high-impact or irreversible workflows. <br>


## Reference(s): <br>
- [I-Lang homepage](https://ilang.ai) <br>
- [I-Lang dictionary](https://github.com/ilang-ai/ilang-dict) <br>
- [I-Lang OpenClaw repository](https://github.com/ilang-ai/ilang-openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/adsorgcn/ilang-compress) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Text notation with a brief Markdown explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compressed I-Lang expressions and explanatory text; examples report about 40-65% token savings.] <br>

## Skill Version(s): <br>
2.3.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
