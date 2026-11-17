## Description:

提供 Khronos 官方 OpenCL 规范、头文件、SDK、CTS 及社区工具的准确下载链接和资源索引。当用户询问 OpenCL 官方文档、API 参考、开发组件获取方式时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[leosaang](https://clawhub.ai/user/leosaang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find Khronos OpenCL specifications, API references, headers, SDK components, conformance tests, and clearly attributed community tools. It helps users choose official resources and obtain setup commands or local organization guidance for OpenCL development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest normal development setup commands that download from Khronos, GitHub, or system package repositories, including package-manager commands.

Mitigation: Review commands before running them, especially sudo package-manager commands, and confirm downloads come from the cited official or attributed project URLs.

Risk: OpenCL resource links and version guidance can become stale over time.

Mitigation: Check the Khronos registry and referenced project repositories before relying on links for release-critical documentation or build inputs.

Risk: Community tools mentioned by the skill are not Khronos-owned resources.

Mitigation: Keep third-party attribution visible and evaluate each community tool's repository, license, and maintenance status before adoption.

## Reference(s):

- [OpenCL API Specification 3.0 Unified](https://registry.khronos.org/OpenCL/specs/3.0-unified/pdf/OpenCL_API.pdf)
- [OpenCL C Language Specification](https://registry.khronos.org/OpenCL/specs/3.0-unified/pdf/OpenCL_C.pdf)
- [OpenCL Extension Registry](https://registry.khronos.org/OpenCL/extensions/)
- [OpenCL Reference Pages](https://registry.khronos.org/OpenCL/sdk/3.0/docs/man/)
- [OpenCL Quick Reference Card](https://www.khronos.org/files/opencl-3-0-quick-reference-card.pdf)
- [OpenCL Official Homepage](https://www.khronos.org/opencl/)
- [Khronos OpenCL Developer Resources](https://www.khronos.org/developers/opencl/)
- [Khronos OpenCL Community Forum](https://community.khronos.org/c/opencl/)
- [KhronosGroup OpenCL-Headers](https://github.com/KhronosGroup/OpenCL-Headers)
- [KhronosGroup OpenCL-CLHPP](https://github.com/KhronosGroup/OpenCL-CLHPP)
- [KhronosGroup OpenCL-ICD-Loader](https://github.com/KhronosGroup/OpenCL-ICD-Loader)
- [KhronosGroup OpenCL-CTS](https://github.com/KhronosGroup/OpenCL-CTS)
- [OpenCL Intercept Layer](https://github.com/intel/opencl-intercept-layer)
- [clspv](https://github.com/google/clspv)
- [clvk](https://github.com/kpet/clvk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with links and optional bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May answer in Chinese by default and may include normal development setup commands for downloading OpenCL resources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
