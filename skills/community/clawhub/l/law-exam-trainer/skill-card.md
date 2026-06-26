## Description: <br>
A Chinese law exam study assistant that turns exam videos, documents, images, and notes into practice questions, answer feedback, mistake explanations, and knowledge-point references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujun2508](https://clawhub.ai/user/lujun2508) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and exam-preparation users use this skill to generate Chinese legal professional qualification exam question banks from uploaded study materials, practice through chat-style answers, and receive explanations for wrong answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded study materials may include sensitive legal or personal information. <br>
Mitigation: Review and redact files before uploading, and avoid using confidential legal or personal material. <br>
Risk: The artifact names a hardcoded local Windows folder for saved question banks. <br>
Mitigation: Update the save path to a folder the user controls before creating or storing question-bank files. <br>
Risk: Generated practice questions and legal explanations may be incomplete or misleading. <br>
Mitigation: Use outputs for study support and verify legal conclusions against authoritative materials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lujun2508/law-exam-trainer) <br>
- [法考相关开源资源](references/resources.md) <br>
- [fighting41love/funNLP](https://github.com/fighting41love/funNLP) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or chat-style text containing generated questions, answer feedback, mistake explanations, and knowledge-point references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process uploaded study materials; the artifact names a local Windows question-bank folder that should be changed to a controlled location before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
