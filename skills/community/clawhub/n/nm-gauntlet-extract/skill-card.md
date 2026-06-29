## Description: <br>
Builds the gauntlet knowledge base from AST extraction and AI enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to initialize or refresh a local `.gauntlet/knowledge.json` knowledge base for a codebase. It supports codebase challenge preparation by combining AST extraction, AI-enriched explanations, cross-references, preserved annotations, and coverage reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated knowledge file can summarize private or sensitive codebase details. <br>
Mitigation: Run the skill only on intended repositories and review `.gauntlet/knowledge.json` before committing or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-gauntlet-extract) <br>
- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and a JSON knowledge file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes `.gauntlet/knowledge.json` in the target repository and reports category coverage, gaps, and difficulty distribution.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence; skill frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
