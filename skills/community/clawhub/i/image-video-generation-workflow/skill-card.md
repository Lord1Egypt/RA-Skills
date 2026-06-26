## Description: <br>
Guides developers through a local image and video generation workflow using ComfyUI-style generation entry points, browser review loops, source-pack research, and reusable prompt or workflow capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeman840425-del](https://clawhub.ai/user/codeman840425-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to establish a repeatable local loop for generating, reviewing, and refining image or video outputs while separating executable workflow sources from inspiration and tutorial material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Referenced GitHub projects or local generation servers may request permissions or introduce separate supply-chain risk. <br>
Mitigation: Review each referenced tool's provenance and permissions separately, run it in a project-specific workspace, and approve execution steps explicitly. <br>
Risk: Tutorial and inspiration sources can be mistaken for authoritative implementation instructions. <br>
Mitigation: Use GitHub references for executable entry points, video references for demonstrations, and Flickr only for visual inspiration. <br>
Risk: Changing several prompts, parameters, or models at once can make results hard to compare or reproduce. <br>
Mitigation: Run a minimal loop first, change one prompt or parameter group at a time, and record keep, discard, or rerun decisions. <br>


## Reference(s): <br>
- [MeiGen AI Design MCP](https://github.com/jau123/MeiGen-AI-Design-MCP) <br>
- [mcp-image](https://github.com/shinpr/mcp-image) <br>
- [z-image-studio](https://github.com/iconben/z-image-studio) <br>
- [YouTube workflow reference](https://www.youtube.com/watch?v=7aEQnTsI6zs) <br>
- [Bilibili workflow reference](https://www.bilibili.com/video/BV14mrfBSEdq/) <br>
- [Flickr visual reference](https://www.flickr.com/photos/dianeworland/55055024432/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with ordered workflow steps, guardrails, and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill itself is a workflow guide and does not generate files, execute code, or handle credentials.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
