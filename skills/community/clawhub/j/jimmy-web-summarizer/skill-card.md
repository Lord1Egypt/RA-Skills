## Description: <br>
Fetch and summarize web pages for AI agents. Extract key information from URLs and return structured markdown summaries. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmyclanker](https://clawhub.ai/user/jimmyclanker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public web pages and produce concise structured markdown summaries for research, memory, and fact checking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to URLs supplied by the user or agent. <br>
Mitigation: Use it only with public web pages and avoid localhost, private network, cloud metadata, or sensitive URLs. <br>
Risk: The artifact claims robots.txt handling, but the security guidance says not to rely on that claim unless the script is updated to enforce it. <br>
Mitigation: Confirm robots.txt requirements separately before using the skill against sites where crawler policy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimmyclanker/jimmy-web-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Structured markdown summary with key points, source URL, and generation timestamp] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches a user-provided URL over outbound HTTP(S); no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
