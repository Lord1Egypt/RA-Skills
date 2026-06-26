## Description: <br>
Bilingual search-layer skill for OpenClaw that turns ordinary web lookup into multi-source retrieval, intent-aware ranking, adaptive weighting, thread-pulling research, Chinese-query optimization, and finance-aware realtime prioritization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wewehg](https://clawhub.ai/user/wewehg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to broaden web lookup into ranked multi-source research, Chinese-language search, comparison work, status/news checks, and finance-aware realtime quote retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call several external search and market-data providers, which may expose user queries or URLs to third-party services. <br>
Mitigation: Use low-scope dedicated provider keys and avoid confidential queries, private URLs, or sensitive internal data. <br>
Risk: The skill can reuse local OpenClaw search credentials and automatically use GitHub credentials found on the machine. <br>
Mitigation: Review local credential files and environment variables before use, and prefer tokens with the minimum required scope. <br>
Risk: Recursive thread-pulling and broad fetching can retrieve more external content than expected. <br>
Mitigation: Review depth and thread-fetching settings before deep research workflows and inspect results before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wewehg/openclaw-glasses) <br>
- [Publisher profile](https://clawhub.ai/user/wewehg) <br>
- [Intent guide](references/intent-guide.md) <br>
- [Authority domains](references/authority-domains.json) <br>
- [Research-light regression samples](references/research-light-regression-samples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, or shell command guidance depending on the workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked search results, citations, extracted thread references, or realtime quote snippets.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
