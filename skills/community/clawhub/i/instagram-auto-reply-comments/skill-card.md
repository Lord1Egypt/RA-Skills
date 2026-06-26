## Description: <br>
Automate Instagram comment-to-DM funnels using the Upload-Post API for keyword-triggered private replies, lead capture, one-shot comment scans, persistent monitors, and DM follow-up workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mutonby](https://clawhub.ai/user/mutonby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and agents use this skill to configure Instagram comment funnels, send private replies to commenters, monitor replies, and report funnel metrics through Upload-Post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated DMs can contact every commenter if trigger keywords are omitted or the target post is wrong. <br>
Mitigation: Confirm the exact post, trigger keywords, message text, monitoring interval, and persistence before starting a funnel. <br>
Risk: Persistent monitors can continue sending DMs after the agent session ends. <br>
Mitigation: Review monitor status and logs, then stop or delete monitors when the campaign is finished. <br>
Risk: The Upload-Post API key grants access to connected Instagram messaging workflows. <br>
Mitigation: Keep UPLOAD_POST_API_KEY private and provide it only in a trusted execution environment. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/mutonby/instagram-auto-reply-comments) <br>
- [Upload-Post homepage](https://upload-post.com) <br>
- [Upload-Post API docs](https://docs.upload-post.com) <br>
- [Upload-Post LLM reference](https://docs.upload-post.com/llm.txt) <br>
- [Meta Compliance Reference](references/compliance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request examples, monitor identifiers, funnel status, logs, and metrics such as comments scanned and DMs sent.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
