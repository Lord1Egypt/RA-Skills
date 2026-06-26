## Description: <br>
An information retrieval assistant for GaoKao regional score lines, designed to help candidates query admission cut-off scores, admission batches, and corresponding rankings across different regions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhl-det](https://clawhub.ai/user/jhl-det) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External candidates, families, and education advisors use this skill to look up GaoKao regional admission score lines, admission batches, and rankings by province, year, subject track, and batch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup filters are sent to Tencent's GaoKao endpoint. <br>
Mitigation: Avoid including unnecessary personal information in prompts or lookup parameters. <br>
Risk: The trigger phrase is broad and may activate on unrelated score-line queries. <br>
Mitigation: Review whether the user's request is about GaoKao regional score lines before using the skill's result. <br>
Risk: Admission score-line data can be stale or mismatched if the inferred province, year, subject track, or batch is wrong. <br>
Mitigation: Confirm ambiguous lookup filters with the user and cite the queried filters in the response. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jhl-det/province-score-line) <br>
- [Tencent GaoKao score-line data page](https://m.gaokao.cn/proscore?fromcoop=sougou) <br>
- [Tencent GaoKao lookup endpoint](https://gaokao.search.qq.com/skills_data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise natural-language answers, with shell command invocation when the helper script is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers are based on matched province, year, subject track, and admission batch filters.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
