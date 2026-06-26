## Description: <br>
根据论文链接（arXiv / Google Scholar / Nature 等）自动抓取全部作者列表，并行搜集每位作者的公开信息（所在机构、研究方向、教育背景、Google Scholar / GitHub / LinkedIn / 个人主页），生成双 Sheet Redoc 在线文档：Sheet1 为作者个人信息表（含账号链接），Sheet2 为按学校背景分组汇总。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mc6680000](https://clawhub.ai/user/mc6680000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and agents use this skill to collect public author profile information for large multi-author papers and organize it into a two-sheet Redoc document for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review verdict is suspicious and flags powerful maintenance workflows in the reviewed skill set. <br>
Mitigation: Install only in a trusted ClawHub maintainer environment and review behavior before enabling the skill. <br>
Risk: Review helpers may run with relaxed sandboxing or send code diffs to external model tools. <br>
Mitigation: Use sandbox-preserving review settings when available and avoid sending sensitive code or data to external tools. <br>
Risk: The skill collects public author profile information from the web, which may be stale or ambiguous. <br>
Mitigation: Use public sources only, omit private contact details, and mark unconfirmed affiliations or background information as pending confirmation. <br>


## Reference(s): <br>
- [Semantic Scholar Graph API paper authors endpoint](https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=authors) <br>
- [ClawHub skill page](https://clawhub.ai/mc6680000/paper-author-profiler-redoc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions for producing a two-sheet Redoc author profile document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs public author profile fields and grouped school-background summaries; unavailable or unconfirmed information is marked for confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
