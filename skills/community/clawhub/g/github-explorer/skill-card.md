## Description: <br>
Deep-dive analysis of GitHub projects, covering architecture, community health, competitive landscape, and cross-platform knowledge sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical evaluators use this skill to investigate GitHub repositories before adoption or comparison. It gathers repository metadata, issues, commits, community discussion, related knowledge sources, and alternatives, then produces a structured project assessment report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect private or sensitive repository content when a request is vague. <br>
Mitigation: Limit what may be inspected or shared, and ask the agent to confirm before using web access or analyzing a repository. <br>
Risk: Repository assessments can be incomplete or misleading if upstream web, GitHub, or community sources are unavailable or stale. <br>
Mitigation: Review cited links and source freshness before relying on the report for adoption, security, or purchasing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tom859174-sketch/github-explorer) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [openclaw-skills aggregate repository](https://github.com/blessonism/openclaw-skills) <br>
- [search-layer dependency](https://github.com/blessonism/openclaw-search-skills/tree/main/search-layer) <br>
- [content-extract dependency](https://github.com/blessonism/openclaw-search-skills/tree/main/content-extract) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown structured report with repository links, sourced discussion summaries, and inline shell commands where collection steps are described] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are expected to include concrete source links, repository health signals, selected issues, limitations, competitor comparisons, knowledge-source checks, and a final judgment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
