## Description: <br>
噗滋（pozzzi）慈善 - 帮助中小型 NGO 生成日常行政文书，支持合同协议、会议纪要、公函、感谢信和工作计划五类文书，内置固定法律条款直通机制避免模型改写关键条款。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
NGO staff and administrators use this skill to draft routine operational documents such as contracts, meeting minutes, official letters, thank-you letters, and work plans. It is intended to produce review-ready drafts with required disclaimers and fixed contract clauses preserved outside model generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft document content may be sent to the user's chosen model provider. <br>
Mitigation: Confirm the chosen provider is acceptable for the document content before use and avoid submitting unnecessary personal or sensitive data. <br>
Risk: Generated contracts, letters, meeting minutes, and plans may contain inaccurate or incomplete formal guidance. <br>
Mitigation: Require human review before use, and have legal or formal documents reviewed by a qualified person. <br>
Risk: User inputs may contain personal data, especially minors' data. <br>
Mitigation: Avoid unnecessary personal data, do not process minors' data, and use the skill's validation and PII-filtering workflow as a gate before model calls. <br>
Risk: Local generation metadata may remain on the device. <br>
Mitigation: Confirm local retention is acceptable for the organization and avoid storing prompt text or generated document bodies in logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aikawabigsky309/pozzzi-charity-document) <br>
- [Ministry of Civil Affairs reference used by volunteer agreement template](https://www.mca.gov.cn/article/yw/hjzcbz/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown document drafts with injected AI-use and disclaimer notices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated document metadata such as model/provider, duration, degradation status, and fixed-clause count; formal or legal documents require human review before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
