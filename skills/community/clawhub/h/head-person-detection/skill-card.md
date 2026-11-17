## Description:

输入一张图像，对其中的人头人体进行检测，输出图片中所有目标的检测框、置信度和标签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit an image by URL or base64 data and receive head and person detections with bounding boxes, confidence scores, and labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends image URLs or base64 image data to a remote XiaoBenYang API.

Mitigation: Use only images that are appropriate to share with that service and review privacy requirements before deployment.

Risk: The skill stores XBY_APIKEY in a local plaintext .env file.

Mitigation: Use a dedicated low-privilege API key, keep .env out of source control and shared exports, and rotate the key if the workspace may have been shared.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/alinklab/skills/head-person-detection)
- [ALinkLab publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown summary of JSON detection results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns raw API data including detection boxes, confidence scores, and labels.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
