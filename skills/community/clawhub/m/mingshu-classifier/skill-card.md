## Description: <br>
Classifies and labels files under a target directory by scanning filenames and supported file contents for personal-information sensitivity under GB/T 35273 rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkming1998](https://clawhub.ai/user/kkming1998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and compliance teams use this skill to scan local directories, identify files that may contain sensitive or general personal information, and produce reviewable classification results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect filenames and supported file contents in a selected local directory, and exported reports may reveal sensitive paths or matched keywords. <br>
Mitigation: Choose a narrow target directory, use --name-only when content inspection is unnecessary, and treat terminal, CSV, and JSON results as sensitive. <br>
Risk: Keyword-based classifications are advisory and may be incomplete or overinclusive. <br>
Mitigation: Review classifications against actual file contents before using results for compliance, access-control, or handling decisions. <br>
Risk: PDF and legacy .doc files are not read for content and are classified from filenames only. <br>
Mitigation: Inspect unsupported formats separately or convert them to a supported format before relying on the classification. <br>


## Reference(s): <br>
- [GB/T 35273 file classification keyword rules](references/classification_rules.md) <br>
- [ClawHub release page](https://clawhub.ai/kkming1998/mingshu-classifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with terminal output and optional CSV or JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include file paths, matched keywords, category labels, match source, and handling suggestions.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
