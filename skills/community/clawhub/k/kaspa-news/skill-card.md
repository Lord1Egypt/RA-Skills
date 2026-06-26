## Description: <br>
Kaspa News lets an agent fetch public Kaspa ecosystem news, core development updates, ecosystem launches, community discussions, videos, Reddit posts, and pulse summaries from kaspa.news without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atl4so](https://clawhub.ai/user/atl4so) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve current Kaspa-related news, social updates, videos, Reddit posts, and pulse reports from public kaspa.news endpoints. It is intended for live retrieval when a user asks what is happening in the Kaspa ecosystem now. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts kaspa.news for live public Kaspa updates when invoked. <br>
Mitigation: Use it only when live Kaspa retrieval is intended; for generic Kaspa discussion, instruct the agent not to invoke this skill. <br>
Risk: Returned news and social content is time-sensitive public data and may need verification before use. <br>
Mitigation: Check the provided source links before relying on important claims or making decisions from the output. <br>


## Reference(s): <br>
- [Kaspa News ClawHub page](https://clawhub.ai/atl4so/kaspa-news) <br>
- [kaspa.news public API](https://kaspa.news/api) <br>
- [FORMAT_LOCK.md](FORMAT_LOCK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text with Markdown source links; JSON when the --json option is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 with requests, jq, and network access to public kaspa.news endpoints; no credentials are required.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
