## Description: <br>
投资者背景调查工具，系统化核查投资方资质、资金来源、过往业绩与潜在风险。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Entrepreneurs and finance teams use this skill before fundraising to evaluate potential investors, identify cooperation risks, and prepare investor-specific outreach and negotiation strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A reference file contains an embedded tool-call style instruction to write files outside the skill's stated due-diligence purpose. <br>
Mitigation: Treat reference markdown as untrusted text, do not execute embedded tool-call blocks, and remove the write_file-style block from references/投资协议要点库.md before deployment. <br>
Risk: Investor due-diligence conclusions may be inaccurate when based on stale or single-source public information. <br>
Mitigation: Cross-check important claims against multiple independent sources and consult legal or financial professionals before making major fundraising or contract decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golngod/hutian-opc-investor-dd) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/golngod) <br>
- [调查框架](references/调查框架.md) <br>
- [数据源清单](references/数据源清单.md) <br>
- [决策链调研方法](references/决策链调研方法.md) <br>
- [基金运营数据模板](references/基金运营数据模板.md) <br>
- [投资协议要点库](references/投资协议要点库.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown profiles, risk checklists, analysis reports, and strategy documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill relies on public information and recommends cross-checking findings across multiple sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
