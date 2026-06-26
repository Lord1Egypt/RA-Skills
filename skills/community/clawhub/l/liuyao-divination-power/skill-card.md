## Description: <br>
Provides Liuyao Najia divination charting and step-by-step interpretation for a stated question, including optional report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanding1998](https://clawhub.ai/user/seanding1998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run Liuyao divination charting and interpretation for a question, producing staged analysis and a shareable report. It supports automatic chart generation as well as interpretation from supplied chart JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save the user's question and analysis as local report files, usually under ~/Desktop. <br>
Mitigation: Do not use private questions unless local storage is acceptable, and delete the generated report directory after use if the question is sensitive. <br>
Risk: The skill may offer to install the optional sxtwl package for higher-precision calendar calculations. <br>
Mitigation: Use the pure-Python fallback when package installation is not desired or cannot be reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanding1998/liuyao-divination-power) <br>
- [Skill README](README.md) <br>
- [Change log](CHANGELOG.md) <br>
- [Wuxing shengke reference](references/wuxing-shengke.md) <br>
- [Bagua leixiang reference](references/bagua-leixiang.md) <br>
- [Dizhi relations reference](references/di-zhi-relations.md) <br>
- [HTML report guide](references/html-report-guide.md) <br>
- [Jiegua xiangjie reference](references/jie-gua-xiang-jie.md) <br>
- [Liuqin liushen leixiang reference](references/liuqin-liushen-leixiang.md) <br>
- [Sixty-four gua reference](references/64-gua.md) <br>
- [Sixty-four gua usage reference](references/64-gua-yongfa.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, files, guidance] <br>
**Output Format:** [Conversational text, markdown step files, structured chart JSON, and standalone HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local report artifacts, usually under the user's Desktop, and may use an optional sxtwl dependency for higher-precision calendar calculations.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
