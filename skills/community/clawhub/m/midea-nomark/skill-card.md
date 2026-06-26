## Description: <br>
Parses supported short-video and social-media share links and returns watermark-free video, cover, author, and image-gallery information for platforms such as Douyin, Kuaishou, Xiaohongshu, Weibo, Xigua, Doubao, Yunque, and Bilibili. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[mackjosn](https://clawhub.ai/user/mackjosn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to parse supported video or image share links and retrieve downloadable, watermark-free media URLs and related metadata. The artifact describes personal learning and research use rather than commercial deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes an unverified local parser binary. <br>
Mitigation: Install only after trusting the publisher and independently verifying the parser binary source. <br>
Risk: The optional HTTP service may expose parsing functionality outside the intended host if network access is misconfigured. <br>
Mitigation: Run the service on localhost only and do not expose it to a broader network unless access controls and network boundaries are understood. <br>
Risk: Private or token-bearing share links could disclose sensitive access information to the parser. <br>
Mitigation: Use only public share links or links that do not contain private access tokens. <br>
Risk: Parsed media links are temporary and may stop working as platform interfaces change. <br>
Mitigation: Verify parsed results before relying on them and expect periodic parser updates for platform changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mackjosn/midea-nomark) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown with URLs and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful parsing returns title, author details, direct video URL, cover URL, and image count when available; parsed media links may be temporary.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
