## Description: <br>
Helps agents create and review Hearts of Iron IV mods, including focus trees, ideas, characters, events, decisions, localisation, variables, and debugging guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gym114514](https://clawhub.ai/user/gym114514) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, modders, and agents use this skill to draft, inspect, and troubleshoot Hearts of Iron IV mod content such as focus trees, national spirits, events, decisions, localisation files, scripted effects, and validation checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HOI4 mod files may contain incorrect syntax, invalid IDs, encoding mistakes, or balance issues. <br>
Mitigation: Review generated files, use the bundled validation checklist, and test the mod in a HOI4 workspace before release. <br>
Risk: Server metadata includes crypto and purchase capability tags that appear unrelated to the static HOI4 reference content. <br>
Mitigation: Treat those tags as a metadata issue and correct them before relying on the tags for policy or install decisions. <br>
Risk: Broad trigger wording may activate the skill outside the intended HOI4 modding context. <br>
Mitigation: Install and invoke it as a HOI4-specific reference skill and review activation context before using generated content. <br>


## Reference(s): <br>
- [Hearts of Iron IV Modding Wiki](https://hoi4.paradoxwikis.com/Modding) <br>
- [Focus Complete Guide](references/focus_complete_guide.md) <br>
- [Quick Reference](references/quick_reference.md) <br>
- [Vanilla Focus Trees Index](references/vanilla_focus_trees/README.md) <br>
- [Focus Tree Design Guide](examples/09_focus_tree_design_guide.md) <br>
- [HOI4 Modding Validation Checklist](tools/validator.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HOI4 script snippets, configuration examples, validation checklists, and shell or PowerShell commands when useful.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated mod files and snippets should be reviewed and tested in a HOI4 mod workspace before use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence, SKILL.md frontmatter, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
