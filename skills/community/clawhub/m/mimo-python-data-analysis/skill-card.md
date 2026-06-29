## Description: <br>
自动生成并执行 Python 数据分析代码，输出可视化图表和有数据支撑的中文分析结论。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data analysts, researchers, business analysts, and Python learners use this skill to inspect CSV, Excel, JSON, clipboard, URL, or simulated data; generate Python analysis code; run statistical, regression, clustering, time-series, cleaning, and visualization workflows; and receive Chinese reports with chart outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates and runs local Python against user-provided data, which can expose sensitive files or secrets if the user supplies them. <br>
Mitigation: Use only data needed for the analysis, review requests involving sensitive files, internal URLs, authenticated API links, or secrets, and rely on the documented local-processing boundary. <br>
Risk: Optional URL or API data loading can reach internal or authenticated resources when a user provides those inputs. <br>
Mitigation: Confirm that each URL or API source is intended for analysis before execution and avoid providing credentials unless they are genuinely required. <br>
Risk: Large or poor-quality datasets can produce unreliable results or excessive local resource use. <br>
Mitigation: Apply the documented data checks: warn on very small samples, report missing values and outliers, sample 100MB-1GB inputs, and refuse inputs over 1GB with batching guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/mimo-python-data-analysis) <br>
- [Detailed analysis reference](artifact/references/details.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [Chinese Markdown reports with Python code blocks and generated PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may create timestamped analysis scripts and output directories, retry failed code up to three times, sample 100MB-1GB datasets, and refuse datasets over 1GB.] <br>

## Skill Version(s): <br>
1.4.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
