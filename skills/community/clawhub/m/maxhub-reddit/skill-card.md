## Description: <br>
Maxhub Reddit helps agents query and analyze public Reddit community data through MaxHub, including subreddit details, posts, comments, user profiles, search results, and trending content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, product teams, and community managers use this skill to inspect Reddit discussions, monitor community sentiment, collect product feedback, and follow subreddit or user activity through read-only MaxHub API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reddit searches, usernames, post IDs, keywords, URLs, and related query context are sent to MaxHub at https://www.aconfig.cn. <br>
Mitigation: Use the skill only for authorized research, disclose the MaxHub data source in outputs, and avoid sending unnecessary personal or sensitive context. <br>
Risk: The skill requires a MAXHUB_API_KEY and may expose it if credentials are copied into prompts, logs, or shared outputs. <br>
Mitigation: Store the API key as a secret environment variable, keep it out of prompts and logs, and rotate it if exposure is suspected. <br>
Risk: Public-user history lookups and comment analysis can still involve privacy-sensitive user-generated content. <br>
Mitigation: Ask for deliberate user confirmation before looking up a specific person's post or comment history, minimize retained data, and avoid using Reddit cookies or session credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-reddit) <br>
- [MaxHub API Service](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [Recipe Index](references/recipes/_index.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl-based API calls and structured data returned by MaxHub APIs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY; performs read-only requests to https://www.aconfig.cn; supports English and Chinese prompts.] <br>

## Skill Version(s): <br>
3.8.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
