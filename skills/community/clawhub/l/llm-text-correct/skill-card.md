## Description: <br>
Corrects Chinese text using pycorrector with KenLM and optional MacBERT refinement, supporting direct text, files, and folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to correct Chinese spelling, similar-character, grammar, and punctuation errors in pasted text or local text-like files. It is intended for Chinese text workflows and can optionally refine results with a MacBERT model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change Python environments and install broad unpinned packages. <br>
Mitigation: Install and run it only in an isolated environment after reviewing dependency behavior. <br>
Risk: The skill can download models and probe local GPU capabilities. <br>
Mitigation: Allow network downloads and hardware probing only in environments where that behavior is acceptable. <br>
Risk: The skill can bulk-process local files and create corrected copies. <br>
Mitigation: Avoid broad private folders or source-code directories, and review generated output files before using them. <br>
Risk: The skill writes local logs while processing text. <br>
Mitigation: Avoid processing sensitive text unless local logging is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangminrui2022/llm-text-correct) <br>
- [shibing624/macbert4csc-base-chinese model](https://huggingface.co/shibing624/macbert4csc-base-chinese) <br>
- [shibing624/chinese-kenlm-klm model](https://huggingface.co/shibing624/chinese-kenlm-klm) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Corrected Chinese text returned inline or written to corrected text files, with command-line status and logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create sibling corrected files or corrected output folders when file or directory paths are provided.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
