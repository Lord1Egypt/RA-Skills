## Description:

通过青虎 AI 将参考短视频拆解为脚本，再改写为商品视频脚本并用 Seedance 2.5 生成成片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

面向短视频创作者、MCN 机构和品牌营销团队，参考热门视频的结构与节奏，改写为适配自有商品的脚本并生成宣传视频。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions install an unpinned package that may change over time.

Mitigation: Review the package and pin a trusted version before installing it.

Risk: Setup guidance asks users to share an API key in chat.

Mitigation: Configure the key locally with qhkit or a secure environment variable; do not paste it into chat.

Risk: The security scan was partial because four local references could not be matched to bundled files.

Mitigation: Review the referenced files and any tools they invoke before installation.

Risk: Reusing source footage or dialogue can copy material the user does not own.

Mitigation: Borrow only the structure and creative approach; use original footage, product assets, and rewritten dialogue.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/autoagc/skills/linkpix-seedance-25-clone)
- [qhkit package on npm](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Video]

**Output Format:** [Markdown with script text, shell commands, and generated video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides original and rewritten script text for review; video generation requires user confirmation before submission.]

## Skill Version(s):

0.1.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
