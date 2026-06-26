## Description: <br>
中文播客雷达 helps agents discover, compare, and curate trending or rising Chinese podcasts and episodes from 中文播客榜 for listener discovery, creator benchmarking, and distribution curation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cellinlab](https://clawhub.ai/user/cellinlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to find ranked Chinese podcast episodes or shows, compare creators, and prepare curated recommendation or distribution lists. The skill favors ranking fields and title signals, with small Xiaoyuzhou enrichment only when a narrowed shortlist needs more context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on external ranking and enrichment data that may be incomplete, stale, or narrower than full-platform podcast coverage. <br>
Mitigation: Present rankings as current signals rather than universal quality judgments, and disclose caveats for missing genre fields or ranking-only evidence. <br>
Risk: Optional Xiaoyuzhou enrichment performs network requests against user-selected URLs and can add more page-derived context than ranking data alone. <br>
Mitigation: Use enrichment only after narrowing to a small shortlist, keep the built-in 20 URL cap, and review the requested URLs before execution. <br>
Risk: The release is third-party and includes Python scripts that make outbound requests. <br>
Mitigation: Follow the clean scan guidance by reviewing the skill instructions and requested access in the target environment before deployment, especially around sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cellinlab/podcast-radar-cn) <br>
- [Project homepage from ClawHub metadata](https://github.com/XiaohuoluFM/xhlfm-skills/tree/main/skills/podcast-radar-cn) <br>
- [API Notes](references/api.md) <br>
- [Output Modes](references/output-modes.md) <br>
- [Title Signals](references/title-signals.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown recommendations with optional shell commands and JSON results from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should synthesize ranking data into task-shaped recommendations rather than dump raw API fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
