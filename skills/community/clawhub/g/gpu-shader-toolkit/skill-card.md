## Description:

GPU Shader Toolkit helps agents provide shader development, conversion, optimization, debugging, and analysis guidance across HLSL, GLSL, MSL, WGSL, ReShade FX, Unity ShaderLab, WebGL, NVIDIA shader cache workflows, DirectX bytecode, game shader archives, and PPSSPP GE dumps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkd](https://clawhub.ai/user/darkd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and graphics engineers use this skill to ask an agent for shader language references, cross-language conversion help, performance optimization guidance, troubleshooting steps, reusable shader templates, and workflows for inspecting compiled shader artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional workflows direct users to clone, build, and run third-party shader analysis tools.

Mitigation: Pin known commits, review or checksum the source, and run tools from a low-privilege sandbox or disposable workspace containing only the shader files intended for analysis.

Risk: Performance optimization guidance can change shader accuracy, portability, or behavior on specific graphics APIs and GPU architectures.

Mitigation: Profile and test changes on the target APIs, drivers, and hardware before adopting them, especially approximate math and platform-specific conversions.

## Reference(s):

- [nvcachetools](https://github.com/therontarigo/nvcachetools)
- [NVIDIA CUDA Repository](https://developer.download.nvidia.com/compute/cuda/repos/)
- [envytools](https://github.com/envytools/envytools/)
- [dx-shader-decompiler](https://github.com/aizvorski/dx-shader-decompiler)
- [PPSSPP Frame Dump Guide](https://github.com/hrydgard/ppsspp/wiki/How-to-create-a-frame-dump)
- [vulkan-shadertoy-launcher](https://github.com/danilw/vulkan-shadertoy-launcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, command snippets, tables, and shader templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes shader language mappings, optimization checklists, debugging workflows, and reverse-engineering procedures.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
