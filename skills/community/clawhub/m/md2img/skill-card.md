## Description: <br>
Convert Markdown, provided as inline text or a `.md` file path, into a single PNG image using local Markdown-to-HTML rendering and a headless browser screenshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[520MianXiangDuiXiang520](https://clawhub.ai/user/520MianXiangDuiXiang520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn Markdown content or Markdown files into a single PNG image, including mobile-width screenshots when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown image references can trigger remote HTTP(S) fetches while rendering. <br>
Mitigation: Render only trusted Markdown or audit image references first; use the no-inline-images option when remote image inlining is not appropriate. <br>
Risk: Markdown can reference absolute local image paths that may be read and embedded into the generated PNG. <br>
Mitigation: Avoid untrusted Markdown in sensitive environments and review image paths before rendering. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [PNG file path with supporting Markdown guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one PNG image; supports configurable image width and optional image inlining control.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
