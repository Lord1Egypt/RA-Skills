## Description: <br>
自动解析 Mplus 输出文件，提取拟合指数和标准化参数，生成符合 APA 标准的图表与可引用的 PDF 分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lz0311-zhen](https://clawhub.ai/user/lz0311-zhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and students in psychology, management, education, and related social-science fields use this skill to turn Mplus CFA or SEM output into fit-index summaries, academic charts, and APA-style PDF reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package asks agents to run scripts that are not included in the artifact. <br>
Mitigation: Verify the actual script paths and contents before allowing execution, and avoid relative scripts/... commands unless they resolve to trusted files. <br>
Risk: Generated statistical interpretations can be incomplete or misleading when required Mplus sections are missing or when significance thresholds need domain-specific adjustment. <br>
Mitigation: Confirm the input contains MODEL FIT INFORMATION and STDYX Standardization sections, then have a qualified researcher review fit thresholds, significance claims, and any multiple-comparison needs before citing the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lz0311-zhen/mplus-report-insight) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and expected PDF report artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces fit-index summaries, APA-style chart descriptions, and guidance for generating PDF reports from Mplus .out files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
