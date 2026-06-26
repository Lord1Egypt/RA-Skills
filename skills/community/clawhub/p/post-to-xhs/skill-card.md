## Description: <br>
Publishes or schedules image and video notes to Xiaohongshu by collecting required content, validating title and media constraints, showing a preview, and publishing only after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmznini](https://clawhub.ai/user/xmznini) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, marketers, and operators use this skill to prepare Xiaohongshu posts, validate required fields and media, preview the final note, and publish or schedule it through the configured publishing integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publishing integration can publish or schedule content under the user's Xiaohongshu account. <br>
Mitigation: Before confirmation, review the logged-in account, title, body, tags, visibility, schedule time, and every image or video path. <br>
Risk: Invalid or unintended media paths can cause failed posts or publish the wrong asset. <br>
Mitigation: Use only the intended image URLs or absolute local video path and verify the previewed media list before approving publication. <br>
Risk: Platform constraints can truncate titles or reject unsupported post formats. <br>
Mitigation: Keep titles within the documented 20-character limit, provide at least one image for image notes, and do not mix image and video media in the same post. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xmznini/post-to-xhs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Conversational text with structured publication parameters and tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before publishing and reports the note ID and publication status after success.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
