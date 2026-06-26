## Description: <br>
Builds the Gauntlet knowledge base from AST extraction and AI enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to create or refresh a local `.gauntlet/knowledge.json` knowledge base for a codebase by extracting AST data, adding natural-language explanations, cross-referencing related entries, and reporting coverage gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or updates `.gauntlet/knowledge.json`, which can overwrite or change local workflow state. <br>
Mitigation: Review or commit the repository state before running the skill and inspect changes to `.gauntlet/knowledge.json` before relying on them. <br>
Risk: The skill may invoke an external Gauntlet extractor script referenced by `CLAUDE_PLUGIN_ROOT`. <br>
Mitigation: Use only a trusted Gauntlet plugin installation and verify `CLAUDE_PLUGIN_ROOT` before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-gauntlet-extract) <br>
- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates `.gauntlet/knowledge.json`, preserves curated annotations in `.gauntlet/annotations/`, and reports summary categories, coverage gaps, and difficulty distribution.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
