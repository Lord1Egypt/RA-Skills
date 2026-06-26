## Description: <br>
Converts structured JSON video material data with oralBroadcastingList, materialList, and bgmInfo into a natural-language Jianying API video description with timelines, subtitles, material matching, BGM, and special requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2719040953](https://clawhub.ai/user/2719040953) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation users use this skill to turn a structured video-material JSON payload into a Jianying-ready production description. It is intended for workflows that need calculated segment timing, subtitle synchronization, media matching, background music details, and user-specified video effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input JSON may contain private media URLs, OSS bucket names, or object keys. <br>
Mitigation: Use only with media assets intended for the downstream Jianying or video system, and avoid providing private URLs or OSS keys unless that system is approved to receive them. <br>
Risk: The workflow references a fixed asset-download domain for constructing media URLs. <br>
Mitigation: Confirm that the referenced asset-download domain is appropriate for the deployment environment before relying on generated asset links. <br>


## Reference(s): <br>
- [JSON schema reference](references/json-schema.md) <br>
- [ClawHub release page](https://clawhub.ai/2719040953/json-to-jianying-description) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style natural-language video description with timeline, subtitle, material, BGM, and special requirement sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include constructed media URLs and timing calculations derived from user-provided JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
