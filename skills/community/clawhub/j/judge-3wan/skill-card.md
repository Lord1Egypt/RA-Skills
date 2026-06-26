## Description: <br>
根据参谋官审核结果判定内容是否合格，并只输出“合格”或“不合格”。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaozha87](https://clawhub.ai/user/xiaozha87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Reviewers and agent workflows use this skill as a final Chinese-language pass/fail judge after a prior reviewer conclusion is available. It converts a conclusion of “合格” or “不合格” into the exact final label with no additional explanation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally suppresses reasoning and context, so downstream users may not see why a result was accepted or rejected. <br>
Mitigation: Use it only after a separate review step has produced a clear conclusion, and keep the prior reviewer output available for audit or dispute handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaozha87/judge-3wan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns exactly one of two Chinese labels: 合格 or 不合格, without explanation or additional text.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
