## Description: <br>
Create and edit JSON Canvas files (.canvas) with nodes, edges, groups, and connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sadlay](https://clawhub.ai/user/sadlay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, writers, and knowledge workers use this skill to create or modify JSON Canvas files for visual canvases, mind maps, flowcharts, project boards, and Obsidian canvas workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editing existing .canvas files can overwrite or corrupt valuable canvas content. <br>
Mitigation: Review diffs or keep backups before applying changes, especially for important canvases. <br>
Risk: Malformed JSON, duplicate IDs, or dangling edge references can make a canvas fail to load or render incorrectly. <br>
Mitigation: Parse the JSON after changes and verify unique IDs, required node fields, valid node types, and all fromNode and toNode references. <br>


## Reference(s): <br>
- [JSON Canvas Spec 1.0](https://jsoncanvas.org/spec/1.0/) <br>
- [JSON Canvas GitHub](https://github.com/obsidianmd/jsoncanvas) <br>
- [JSON Canvas Complete Examples](references/EXAMPLES.md) <br>
- [ClawHub skill page](https://clawhub.ai/sadlay/json-canvas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON Canvas content and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or edit local .canvas files; validates JSON structure, unique IDs, required node fields, edge references, sides, ends, and color values.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
