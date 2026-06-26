## Description: <br>
Researches recent OpenClaw GitHub releases and tags, filters for the previous day's updates, and produces a structured Markdown report with special attention to memory-system changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxin-lixiang](https://clawhub.ai/user/liuxin-lixiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to track OpenClaw release activity, summarize important changes, and generate dated update reports focused on memory, embeddings, LanceDB, SQLite, and related context-management changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports rely on current GitHub release and tag content and may contain incomplete or inaccurate summaries. <br>
Mitigation: Review generated reports against the linked GitHub release or tag before relying on them. <br>
Risk: The skill accesses GitHub and writes generated reports into report_v1/. <br>
Mitigation: Install and run it only where GitHub access and local report-file creation are acceptable. <br>


## Reference(s): <br>
- [OpenClaw GitHub Tags](https://github.com/openclaw/openclaw/tags) <br>
- [ClawHub Skill Page](https://clawhub.ai/liuxin-lixiang/openclaw-update-researcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated reports under report_v1/YYYY-MM-DD/ when a qualifying OpenClaw release is found; otherwise no report is generated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
