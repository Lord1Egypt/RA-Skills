## Description: <br>
Get a daily digest of trending posts from Moltbook with Chinese summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wangfugui1799](https://clawhub.ai/user/Wangfugui1799) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to fetch trending Moltbook posts, translate selected post content into Simplified Chinese, and produce a daily digest for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Moltbook API key to fetch posts. <br>
Mitigation: Use an environment variable or a tightly permissioned credentials file, and prefer a least-privileged Moltbook key if available. <br>
Risk: Selected Moltbook post text may be sent to Google Translate. <br>
Mitigation: Run the skill only when that data sharing is acceptable for the posts being summarized. <br>
Risk: The deep-translator dependency may change behavior across versions. <br>
Mitigation: Pin deep-translator to a reviewed version before routine use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Wangfugui1799/moltbook-daily-digest) <br>
- [Moltbook API Reference](artifact/references/api.md) <br>
- [Moltbook API Base URL](https://www.moltbook.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest with Chinese summaries, post metadata, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Moltbook API key and may use Google Translate through deep-translator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
