## Description: <br>
Expert academic-paper reading skill that extracts text from uploaded PDF, Word, Excel, PowerPoint, or text files and produces structured six-dimension analysis reports in Markdown and Word format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuruitian](https://clawhub.ai/user/xuruitian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and researchers use this skill to deeply read academic papers, extract source text from common document formats, and turn the paper into a structured critical analysis report with practical learning suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private, unpublished, medical, financial, or proprietary papers may be processed and retained in generated local files. <br>
Mitigation: Confirm output paths before running the skill and delete retained extracted text, latest_analysis.json, and Word reports when the analysis is complete. <br>
Risk: The skill includes supplemental web-search guidance even though its README claims no network use. <br>
Mitigation: Disable or forbid web search for sensitive papers unless the user explicitly approves external research. <br>
Risk: Generated academic analysis may be incomplete or misleading if extraction misses content or if the source paper is ambiguous. <br>
Mitigation: Review quoted passages and key findings against the original paper before relying on the report. <br>


## Reference(s): <br>
- [Academic Prompt Template](references/academic_prompt.md) <br>
- [ClawHub release page](https://clawhub.ai/xuruitian/paper-reader-xuruitian) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis report plus generated .docx report; JSON may be used as an intermediate report-generation input.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads uploaded paper files locally and may write extracted text, latest_analysis.json, and a Word report to disk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
