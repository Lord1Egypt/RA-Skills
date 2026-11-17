## Description:

为 MindAR.js 与 A-Frame WebAR 图像识别提供 .mind 编译、目标图质量检查、运行时调优和无头浏览器验证指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

面向构建手机端图像识别 WebAR 体验的开发者，指导其编译 MindAR 目标文件、评估图像可跟踪性、调优跟踪参数，并在无图形界面的环境中验证流程。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Headless browser testing uses SwiftShader flags that enable unsafe software WebGL.

Mitigation: Use these flags only with trusted local test content in a disposable browser profile, keep the browser sandbox enabled, bind the test server to localhost, and stop it after testing.

## Reference(s):

- [MindAR WebAR 图像识别 on ClawHub](https://clawhub.ai/junci003/skills/mindar-webar-image-tracking)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with JavaScript, HTML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
