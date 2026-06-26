## Description: <br>
从小说大纲自动拆解逐章 prompt，支持纯文本、JSON、Markdown 格式大纲，并生成每章写作指令。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shine8592](https://clawhub.ai/user/shine8592) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and agent users use this skill to convert a novel outline into chapter-level prompt files and a structured chapter summary. It is intended for outline parsing and prompt preparation, not for writing or expanding the novel prose itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The parser writes prompt files and chapters.json to the selected output directory, which may overwrite existing files with matching names. <br>
Mitigation: Choose the output directory intentionally and review existing files before running the parser. <br>
Risk: Generated prompts enforce Chinese-only style and other fixed writing constraints that may not match every project. <br>
Mitigation: Review the generated prompts before using them with a novel generation tool. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shine8592/novel-outliner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands] <br>
**Output Format:** [Plain text prompt files and a chapters.json summary file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates one prompt file per parsed chapter and writes chapters.json in the selected output directory.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
