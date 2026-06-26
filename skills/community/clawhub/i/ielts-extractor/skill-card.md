## Description: <br>
Extracts IELTS reading passages and question data from Cambridge IELTS PDFs, including multi-page and two-column layouts, into structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lava-chen](https://clawhub.ai/user/lava-chen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content maintainers use this skill to extract IELTS reading passages and grouped questions from Cambridge IELTS PDFs, then save the results as structured JSON and supporting images for an IELTS practice application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write extracted JSON and image files to local project paths. <br>
Mitigation: Confirm where JSON and images will be written, and review generated files before committing or publishing them. <br>
Risk: PDF inputs may contain content the user is not allowed to process or redistribute. <br>
Mitigation: Use the skill only on PDFs the user is authorized to process. <br>


## Reference(s): <br>
- [JSON Format Specification](references/json-format.md) <br>
- [PDF Extraction Guide](references/pdf-extraction.md) <br>
- [Question Type Standards](references/question-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, JSON, Files] <br>
**Output Format:** [Markdown guidance with Python snippets and structured JSON file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local IELTS tracker JSON files and image assets.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
