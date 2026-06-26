## Description: <br>
Automatically creates and schedules six-slide TikTok slideshows with trending hooks and images linked to affiliate articles using NVIDIA FLUX and Postiz. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonnenberglauramarie-afk](https://clawhub.ai/user/sonnenberglauramarie-afk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content operators and affiliate-site owners use this skill to generate TikTok slideshow concepts, images, captions, and Postiz drafts for configured portals. Users should review drafts and connected account settings before enabling automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes apparent credentials in config.json. <br>
Mitigation: Do not run the packaged config.json; replace it with values from config.example.json and rotate any exposed NVIDIA or Postiz credentials before use. <br>
Risk: The skill can create drafts through Postiz for connected TikTok accounts. <br>
Mitigation: Verify the Postiz base URL and TikTok account IDs, run with --dry-run first, and review generated drafts before enabling scheduled automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sonnenberglauramarie-afk/larry-tiktok-agent) <br>
- [Postiz](https://github.com/gitroomhq/postiz-app) <br>
- [NVIDIA API Catalog](https://build.nvidia.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, images, shell commands, configuration, api calls] <br>
**Output Format:** [CLI output, JSON draft files, generated slide images, and Postiz/TikTok draft API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Six-slide slideshow concepts with captions, hashtags, image paths, and optional scheduled draft creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
