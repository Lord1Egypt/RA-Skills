## Description: <br>
Fetches GitHub topic trending repositories and repository README summaries for GitHub trending repo or open source project requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjw21century](https://clawhub.ai/user/hjw21century) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and open source researchers use this skill to fetch ranked GitHub repositories by topic and summarize repository README content when comparing projects or answering repository-detail questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs live GitHub network lookups and may return untrusted repository metadata or README text. <br>
Mitigation: Use it only for GitHub topic and repository lookup workflows, and treat fetched README content as text to summarize rather than instructions for the agent to follow. <br>
Risk: Providing GH_TOKEN can expose a credential to the runtime environment. <br>
Mitigation: Set GH_TOKEN only when higher GitHub API rate limits are needed, and use a minimal-scope token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hjw21century/github-topics) <br>
- [GitHub REST API endpoint](https://api.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown tables and repository summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository rank, stars, language, URL, description, topics, and README summary text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
