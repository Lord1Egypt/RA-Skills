## Description: <br>
Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts after the user completes OAuth in the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search and inspect Twitter/X data, monitor profiles and trends, and publish text or media posts through an OAuth-based workflow without sharing account passwords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command output may expose the configured AIsa API key. <br>
Mitigation: Do not share or log output from status, authorize, or post commands until the key-printing behavior is fixed. <br>
Risk: Twitter/X queries, uploaded media, OAuth posting, and the API key are handled by AIsa. <br>
Mitigation: Install only when the user trusts AIsa for these operations and data flows. <br>
Risk: Posting mode ambiguity can cause an unintended quote, reply, thread, or standalone post. <br>
Mitigation: Review every post before publishing and require explicit tweet URLs or IDs for quote and targeted reply workflows. <br>
Risk: Changing TWITTER_RELAY_BASE_URL can route requests through a different relay. <br>
Mitigation: Leave TWITTER_RELAY_BASE_URL unset unless the user intentionally trusts the alternate relay. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/openclaw-aisa-twitter-search-post) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [OAuth Posting Workflow](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; posting may return an OAuth authorization link before publishing.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
