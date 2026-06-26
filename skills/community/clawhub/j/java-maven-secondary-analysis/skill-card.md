## Description: <br>
Analyze a Java Maven project delivered as a ZIP archive or a GitLab repository URL for secondary-development scope, class counts, module distribution, product customization traces, invasive modifications, and upgrade pollution risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrliugangqiang](https://clawhub.ai/user/mrliugangqiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect Java Maven projects from ZIP archives or authorized GitLab repositories and produce a structured secondary-development analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The available security summary notes that full artifact content review was not present in the scan inputs. <br>
Mitigation: Review the bundled SKILL.md, scanner script, template, and any install or execution steps before deployment. <br>
Risk: The analysis relies on structural and keyword scanning, so customization findings can be incomplete or require business-context interpretation. <br>
Mitigation: Treat generated reports as first-pass evidence and require human review for important findings, affected file paths, and upgrade-risk conclusions. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/mrliugangqiang/java-maven-secondary-analysis) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mrliugangqiang) <br>
- [Artifact: SKILL.md](artifact/SKILL.md) <br>
- [Artifact: report template](artifact/templates/report.md) <br>
- [Artifact: secondary analysis scanner](artifact/scripts/scan_secondary_analysis.py) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with supporting JSON analysis data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a formal report under business/ and can emit structured scan results for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
