## Description: <br>
章节正文生成器 - 根据章节大纲、Voice Profile 和角色档案构建 LLM 提示词，用于生成章节正文。当需要根据大纲创作具体章节时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and agent workflows use this skill to turn a chapter outline, optional style profile, and optional character files into structured Markdown prompts for drafting novel chapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads local outline, style, and character files and writes to a user-provided output path. <br>
Mitigation: Run it against a dedicated novel project folder and review --book-dir, --outline, and --output before execution. <br>
Risk: The Python dependencies are not pinned in the artifact. <br>
Mitigation: Install in an isolated environment and pin rich and PyYAML versions before long-term or shared use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuzhihui886/novel-writer-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prompt files and CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a chapter outline, optional style.yml, and optional characters/*.yml from a local novel project; writes a Markdown prompt file to the requested output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
