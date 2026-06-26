## Description: <br>
Use this skill when the user wants to turn a long podcast, interview, webinar, or talking-head video into multiple short clips for TikTok, Reels, or YouTube Shorts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arpittiwari24](https://clawhub.ai/user/arpittiwari24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn long-form spoken videos into short-form clips with captions, clip titles, scores, URLs, and timestamps. It is intended for podcast, interview, webinar, and talking-head video repurposing through Subscut. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Subscut API key and may expose credentials if users hard-code secrets in shared files. <br>
Mitigation: Keep SUBSCUT_API_KEY in environment configuration or a secret manager, and avoid committing keys or passing them in shared command logs. <br>
Risk: The skill sends a user-provided video URL to Subscut for processing, which can disclose media content or metadata to the service. <br>
Mitigation: Use public or authorized video URLs, and avoid submitting confidential media unless the user accepts Subscut's handling of that content. <br>
Risk: Generated clips may be prepared for public channels such as TikTok, Reels, or YouTube Shorts. <br>
Mitigation: Keep a human review step before publishing clips publicly, especially for copyrighted, sensitive, or brand-controlled content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arpittiwari24/podcast-clipper-subscut) <br>
- [Publisher profile](https://clawhub.ai/user/arpittiwari24) <br>
- [Subscut agents page](https://subscut.com/agents) <br>
- [Skill README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Tool contract example](artifact/examples/tool-contract.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON clip results from the CLI wrapper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUBSCUT_API_KEY; accepts public or authorized video URLs; returns up to 20 clips with rendered URLs, titles, confidence scores, and timestamps.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
