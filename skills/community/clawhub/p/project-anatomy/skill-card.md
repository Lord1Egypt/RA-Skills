## Description: <br>
文件快速扫描通过生成项目文件索引，让 AI 在打开文件前了解内容并减少重复读取和 token 消耗。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adchina2025](https://clawhub.ai/user/adchina2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create compact Markdown indexes of project files so an agent can decide which files need direct reading. It also supports a specialized expense-directory scan and optional recent Downloads filename checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file indexes may summarize private source files, notes, invoices, or recent Downloads filenames. <br>
Mitigation: Run the skill only on intended folders, configure excludes for secrets or private notes, and review generated .anatomy.md files before sharing them with an agent. <br>
Risk: The optional Downloads scan can surface recent local file names that may be sensitive. <br>
Mitigation: Use --scan-downloads only when recent Downloads filenames should be included in the index. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adchina2025/project-anatomy) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown file index with CLI status text and optional YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes .anatomy.md and a companion cache file; compact, summary, and table formats are supported.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
