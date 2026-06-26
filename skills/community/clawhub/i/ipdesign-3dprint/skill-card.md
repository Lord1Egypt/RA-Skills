## Description: <br>
End-to-end AI-powered pipeline for creating 3D-printable IP character figurines with optional image generation and Blender modeling exportable as STL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and makers use this skill to turn text prompts or reference images into collectible-style character concepts, Blender modeling steps, and 3D-print export commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud image generation modes may send design prompts and require sensitive API keys. <br>
Mitigation: Use only trusted providers, keep API keys in environment variables, and avoid submitting confidential designs unless the selected provider is approved for that data. <br>
Risk: The Blender build script clears the active scene and writes generated files under /tmp/skullpanda_output. <br>
Mitigation: Run it in a fresh or background Blender session and preserve any existing work before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergencescience/ipdesign-3dprint) <br>
- [Google AI Studio](https://aistudio.google.com) <br>
- [Comfy Cloud](https://platform.comfy.org) <br>
- [EvoLink](https://evolink.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of Blender project files and STL/OBJ/3MF exports when the generated scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
