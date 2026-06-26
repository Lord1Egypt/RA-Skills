## Description: <br>
Use local visual memory tools to index and search photos and videos from creator media libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bkennedyshit](https://clawhub.ai/user/bkennedyshit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and OpenClaw users use this skill to index local photo and video libraries, search them with natural-language or visual similarity queries, and return previewable media results while keeping media local unless the user asks otherwise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make selected local photo and video folders searchable, which may expose sensitive local media to the agent workflow. <br>
Mitigation: Index only folders the user explicitly selects, avoid sensitive folders unless they are intended to be searchable, and keep uploaded media as temporary session context unless the user asks to save, index, catalog, or remember it. <br>
Risk: The skill depends on a local MCP server and plugin packages that handle media indexing and session media storage. <br>
Mitigation: Install only after reviewing the mneme-mcp and OpenClaw plugin packages, and use it only if local MCP indexing and temporary session media handling fit the user's environment. <br>
Risk: GPU memory management actions can unload resident Ollama models or hand VRAM to another workflow. <br>
Mitigation: Check GPU status before intensive local tasks and use release, reclaim, or evacuate actions only when the user intends to free or coordinate GPU memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bkennedyshit/mneme-vision) <br>
- [Mneme homepage](https://mneme.nepa-ai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and media result card metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local media paths and previewable media_artifacts.v1 results when the host supports rich output.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact metadata reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
