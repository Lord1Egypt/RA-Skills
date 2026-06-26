## Description: <br>
计算中文姓名和公司名的五格数理、康熙笔画、吉凶解释，并可按规则批量生成名字。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azazlf09](https://clawhub.ai/user/azazlf09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate Chinese personal names, company names, stroke counts, and Five Grid numerology results, or to generate candidate names under the skill's scoring rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Name scoring is numerology behavior and should not be treated as factual prediction or professional advice. <br>
Mitigation: Present results as culturally contextual name-analysis guidance and keep human judgment in the loop for consequential naming decisions. <br>
Risk: Rare-character lookups may download about 3 MB of dictionary data from GitHub or CDN sources. <br>
Mitigation: For restricted environments, prepopulate the cache, disable automatic downloads, or use a pinned checksum-verified dictionary source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/azazlf09/name-wuge) <br>
- [cnk3x/bys 81 numerology data source](https://github.com/cnk3x/bys) <br>
- [breezyreeds/kangxi-strokecount data source](https://github.com/breezyreeds/kangxi-strokecount) <br>
- [Kangxi stroke count CSV CDN source](https://cdn.jsdelivr.net/gh/breezyreeds/kangxi-strokecount@master/kangxi-strokecount.csv) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code] <br>
**Output Format:** [Markdown or plain text name reports, generated name lists, and Python callable outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include simplified/traditional Chinese display, Kangxi stroke counts, Five Grid values, auspiciousness labels, explanations, and scores.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
