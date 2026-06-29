## Description: <br>
雄韬汉字视觉重心分析引擎可对单个汉字进行像素级视觉重心、结构平衡和字体差异分析，并输出文字报告、可选 JSON 数据和可视化 PNG 图片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xtoyun](https://clawhub.ai/user/xtoyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, calligraphy learners, and agents use this skill to run local Hanzi visual-center analysis when users ask about character balance, calligraphy structure, center-of-gravity placement, or font-specific differences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default analysis runs may save generated PNG images in the working directory. <br>
Mitigation: Use --no-png or run the analyzer in a scratch workspace when generated images should not be retained. <br>
Risk: The skill requires npm dependencies including the native canvas package. <br>
Mitigation: Install dependencies in a controlled environment and review dependency policy before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xtoyun/hanzi-center) <br>
- [Hanzi visual center homepage](http://shufa.xtocn.com/汉字视觉重心.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with shell commands; the analyzer can emit text reports, JSON, and optional PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and npm dependencies including canvas; PNG generation is enabled by default and can be disabled with --no-png.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
