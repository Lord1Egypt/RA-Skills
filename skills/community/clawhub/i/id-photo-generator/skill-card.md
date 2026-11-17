## Description:

生成合规证件照（一寸、二寸、小一寸、小二寸、身份证、护照、签证等）以及更换证件照底色。当用户上传人物照片并表达"制作证件照/一寸照/两寸照/换底色/蓝底白底红底证件照/生成标准证件照"等意图时使用。核心原则：必须先检测到且仅检测到一张可用人像才允许生成；未识别人像、人像不合格或疑似翻拍合成时绝不生成，并提示用户重新上传。严禁美颜、磨皮、瘦脸等改变面部特征的操作，不得遮挡痣、疤痕等固有标识。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weslon1987](https://clawhub.ai/user/weslon1987)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要制作标准证件照的用户；引导代理根据用户上传的单人照片生成指定规格和底色的证件照，并在图片不合格时给出重拍提示。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports possible inconsistencies in photo-authenticity and minimum-image-dimension validation.

Mitigation: Before official use, confirm the photo is an original, authentic image and check the output against the receiving authority's requirements.

Risk: The workflow handles sensitive facial photos.

Mitigation: Obtain separate consent before upload, limit retention, delete originals and intermediate files after processing, and do not reuse face data for other purposes.

## Reference(s):

- [Image validation specification](references/validation-spec.md)
- [Photo size and background specifications](references/size-bg-spec.md)
- [Privacy and compliance guidance](references/privacy-compliance.md)
- [ClawHub release page](https://clawhub.ai/weslon1987/skills/id-photo-generator)

## Skill Output:

**Output Type(s):** [Image files, Guidance]

**Output Format:** [JPG photo, with optional PNG, plus Chinese user guidance and warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Photo size, background color, and file-size target follow the selected specification. Successful results include the required disclaimer and any applicable warnings.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
