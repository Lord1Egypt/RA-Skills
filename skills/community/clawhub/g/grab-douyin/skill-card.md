## Description:

Downloads Douyin videos from supported Douyin links or 16-19 digit video IDs through the TikHub API, then prints the resolved video URL or saves an MP4 file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to resolve Douyin short links, full Douyin video URLs, query-parameter IDs, or bare 16-19 digit video IDs and optionally download the corresponding video file. It is intended for Douyin video clips only, not live streams, image carousels, or other video platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a TikHub bearer token and sends Douyin video IDs with that token to TikHub.

Mitigation: Store the token only in the expected local configuration file, avoid exposing it in prompts or logs, and confirm TikHub use is acceptable before running the skill.

Risk: Broad trigger rules may cause the agent to process Douyin-looking text or short links before the user's intent is explicit.

Mitigation: Ask for confirmation before making lookups or downloads, especially when input came from untrusted copied text.

Risk: Short-link resolution and downloads make external network requests and can write MP4 files to disk.

Mitigation: Review the resolved video ID and output directory before downloading, and use a custom output directory when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mfang0126/skills/grab-douyin)
- [TikHub token registration](https://user.tikhub.io/register)
- [TikHub Douyin fetch endpoint](https://api.tikhub.io/api/v1/douyin/web/fetch_one_video)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print a direct video URL or write an MP4 file to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
