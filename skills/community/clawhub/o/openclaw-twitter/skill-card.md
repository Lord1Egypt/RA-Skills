## Description: <br>
Searches and reads X/Twitter profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces, and publishes posts after the user completes OAuth in the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to search Twitter/X data, monitor accounts and trends, inspect social activity, and publish text or media posts through OAuth-authorized workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal command output can expose the AISA API key. <br>
Mitigation: Use a scoped AISA key, avoid shared terminals or logs for status, authorize, and post commands, and rotate the key if it appears in logs. <br>
Risk: Posting workflows can publish text or uploaded media to a public Twitter/X account after OAuth authorization. <br>
Mitigation: Authorize only the intended account and review the exact text, media, reply target, or quote URL before running a publish command. <br>
Risk: Uploaded media and post content are sent to AIsa and may become public if publishing succeeds. <br>
Mitigation: Upload only files and text that are approved for the intended audience and acceptable to share with the relay service. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/0xjordansg-yolo/openclaw-twitter) <br>
- [Publisher Profile](https://clawhub.ai/user/0xjordansg-yolo) <br>
- [Posting Workflow Reference](references/post_twitter.md) <br>
- [OpenClaw Homepage](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON responses and inline shell or Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to AIsa Twitter/X API endpoints; posting may return OAuth authorization links or publish results with tweet IDs or links.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
