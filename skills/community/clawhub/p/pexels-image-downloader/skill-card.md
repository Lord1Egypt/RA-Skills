## Description: <br>
Uses the Pexels API to search for and download high-quality free images, with automatic resizing and format validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glittering](https://clawhub.ai/user/Glittering) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, social media teams, and developers can use this skill to retrieve Pexels images for publishing workflows and resize them for target platforms such as Xiaohongshu, WeChat, Weibo, Instagram, Twitter, and Facebook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Pexels API key and sends image search queries to Pexels. <br>
Mitigation: Use a dedicated API key, avoid exposing it in shared terminals or logs, and only run searches that are appropriate to send to Pexels. <br>
Risk: The downloader writes image and metadata files to the local filesystem. <br>
Mitigation: Run it in a dedicated output folder and review downloaded files and generated metadata before using them in production content. <br>
Risk: The artifact depends on requests and Pillow for network access and image processing. <br>
Mitigation: Install pinned or current patched dependency versions and update them through normal security maintenance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Glittering/pexels-image-downloader) <br>
- [Pexels API Documentation](https://www.pexels.com/api/documentation/) <br>
- [Pexels API](https://www.pexels.com/api/) <br>
- [Pillow Documentation](https://pillow.readthedocs.io/) <br>
- [Google Image Optimization Guidance](https://developers.google.com/speed/docs/insights/OptimizeImages) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for searching, downloading, resizing, validating, and organizing local image files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
