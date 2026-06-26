## Description: <br>
Generates structured Feishu interview question documents from candidate resumes and appends comprehensive evaluations from interview transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[funkeyyou](https://clawhub.ai/user/funkeyyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting and hiring teams use this skill to prepare candidate-specific interview questions for WePlay activity operations roles and to turn interview transcripts into structured evaluations. It supports resume review, product-context questions, Japanese oral assessment prompts, and post-interview scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can store and share sensitive candidate data in Feishu using hardcoded folder and collaborator targets. <br>
Mitigation: Verify the Feishu account, folder, collaborator, document permissions, and retention expectations before using the skill with real candidate data. <br>
Risk: The workflow depends on a Feishu helper script that is referenced by the artifact but not included for review. <br>
Mitigation: Review or replace the Feishu helper before deployment, and confirm it handles authentication, permissions, and document writes as expected. <br>


## Reference(s): <br>
- [Question Template](references/question-template.md) <br>
- [Evaluation Template](references/evaluation-template.md) <br>
- [WePlay Product Framework](https://wepie.feishu.cn/wiki/Q62TwQ3Fsi5Q8kkc0iDcINsSnno) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown interview-question and evaluation content with Feishu document creation or append commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include candidate-specific questions, Japanese oral exam prompts, Feishu document URLs, and structured interview evaluation ratings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
