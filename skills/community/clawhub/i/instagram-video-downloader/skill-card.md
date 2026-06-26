## Description: <br>
Download Instagram videos, Reels, and IGTV in HD quality. Free tier: 5 downloads/day. Unlimited downloads for $0.1 per video. Use when user provides an Instagram video URL. Powered by savefbs.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankchen622](https://clawhub.ai/user/frankchen622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when they have a public Instagram video, Reel, post, IGTV item, or story URL and want downloadable video links returned through the savefbs.com service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted Instagram URLs are sent to savefbs.com for processing. <br>
Mitigation: Use only public, non-sensitive Instagram URLs and do not provide Instagram credentials, private links, session URLs, or sensitive content. <br>
Risk: The skill keeps a local usage counter for daily quota tracking. <br>
Mitigation: Install only if local quota tracking is acceptable and review or remove the local usage file when decommissioning the skill. <br>
Risk: The payment and upgrade flow is present, but the artifacts do not show reliable payment verification or a clear unlock process. <br>
Mitigation: Treat payment links cautiously and verify upgrade terms outside the skill before sending funds. <br>


## Reference(s): <br>
- [savefbs.com](https://savefbs.com) <br>
- [savefbs.com pricing](https://savefbs.com/pricing) <br>
- [ClawHub release page](https://clawhub.ai/frankchen622/instagram-video-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command usage and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns download metadata, direct media URLs, usage counts, remaining free quota, and upgrade information when quota is low or exhausted.] <br>

## Skill Version(s): <br>
1.2.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
