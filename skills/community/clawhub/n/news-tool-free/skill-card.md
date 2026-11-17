## Description: <br>
A personalized news briefing skill that learns a user's interest, format, and timing preferences, stores profile and history files locally, and guides an agent to search multiple sources for concise Markdown news summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External personal users, students, and independent developers use this skill to set up local news preferences and receive concise personalized news briefings based on web search and saved interest history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps a local profile and briefing history under ~/news, which may reveal the user's interests if the device or files are shared. <br>
Mitigation: Review, restrict access to, or delete ~/news files when retained preferences or reading history are not desired. <br>
Risk: Generating briefings uses web search, so search terms based on user interests may be sent to external search providers. <br>
Mitigation: Avoid entering sensitive topics, and use search tooling or network settings appropriate for the user's privacy needs. <br>
Risk: News results can be incomplete, stale, conflicting, or unavailable behind login and paywall restrictions. <br>
Mitigation: Cross-check important or controversial items against multiple sources and label source and time in generated briefings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/news-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings, plain-text prompts, and local Markdown configuration/history files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefings are personalized from local preference files and current web search results.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
