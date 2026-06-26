## Description: <br>
YouTube public video and channel data analysis skill that uses the MaxHub API to query video details, comments, captions, playback and stream information, channel profiles, channel videos, Shorts, posts, search, trending videos, and related videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, content researchers, and creator operations teams use this skill to gather and analyze YouTube video, channel, comment, caption, search, trend, and related-content data through MaxHub. It is suited for content research, channel profiling, subtitle corpus collection, comment analysis, topic selection, and competitive monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube IDs, URLs, search terms, and the MaxHub API key to https://www.aconfig.cn. <br>
Mitigation: Use the skill only when that third-party data flow is acceptable, minimize submitted data, and keep MAXHUB_API_KEY out of logs and conversation output. <br>
Risk: Stream and signed URL features may provide media access rather than simple metadata. <br>
Mitigation: Use media-access features only for authorized content and follow applicable platform, copyright, and organizational policies. <br>
Risk: Optional cookies or session credentials can expose account access if production credentials are supplied. <br>
Mitigation: Avoid production cookies or session credentials; use separate test credentials when cookie-backed workflows are necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiewxx/maxhub-youtube) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [Agent recipes index](references/recipes/_index.md) <br>
- [Endpoint whitelist](references/endpoints_whitelist.yaml) <br>
- [Parameter mappings](references/param-mappings.md) <br>
- [Video endpoints](references/video.md) <br>
- [Channel endpoints](references/channel.md) <br>
- [Search endpoints](references/search.md) <br>
- [Comments endpoints](references/comments.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MaxHub API workflows require MAXHUB_API_KEY and curl; outputs should disclose the third-party data source and avoid exposing secrets.] <br>

## Skill Version(s): <br>
3.8.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
