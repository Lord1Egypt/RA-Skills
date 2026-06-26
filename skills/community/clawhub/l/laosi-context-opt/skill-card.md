## Description: <br>
上下文窗口优化器 - 原创技能。智能管理AI上下文窗口，自动压缩历史、去除冗余、保留关键信息，节省token提升效率。适用于长会话、多文件、大项目等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI users use this skill to summarize long conversations, reduce redundant context, preserve key decisions and task state, and produce a concise optimization report for continued work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Context compression can omit details that later turns may still need. <br>
Mitigation: Review the optimization report before replacing working context, and keep L1 items such as user preferences, project configuration, architecture decisions, completed work, and open todos. <br>
Risk: Summaries can overstate quality improvements or token savings when example metrics are treated as guarantees. <br>
Mitigation: Treat token counts and quality scores as task-specific estimates and verify important retained facts against the original conversation when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-context-opt) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown optimization report with retained items, discarded items, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include illustrative token counts, priority tiers, compression triggers, and context-retention recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
