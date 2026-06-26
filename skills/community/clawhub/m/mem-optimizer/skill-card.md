## Description: <br>
Optimizes and summarizes agent memory files to reduce token use, with self-improving preferences, multi-agent checks, and scheduled reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doony15](https://clawhub.ai/user/doony15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preview or run token statistics and compression for memory files, including scheduled daily summaries and optional multi-agent memory optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled or non-dry-run optimization can rewrite memory files and reduce retained detail. <br>
Mitigation: Review dry-run output first, keep scheduled runs disabled until reviewed, and back up memory files before enabling writes. <br>
Risk: Multi-agent and host-status reporting can expose activity from other agents or the runtime environment. <br>
Mitigation: Use only in environments where cross-agent visibility is authorized and external reporting has been reviewed. <br>


## Reference(s): <br>
- [ClawHub Mem Optimizer release](https://clawhub.ai/doony15/mem-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON tool responses and Markdown summary reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes token counts, processed-file details, dry-run status, and optional multi-agent summary reports.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
