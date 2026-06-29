## Description: <br>
Adds developer-authored annotations to the gauntlet knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to capture project-specific rationale, history, and rules as local Gauntlet knowledge annotations for future agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated annotations may include sensitive internal rationale or project history. <br>
Mitigation: Review generated YAML under .gauntlet/annotations/ and redact sensitive content before keeping it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-gauntlet-curate) <br>
- [Gauntlet Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [YAML annotation file plus concise text confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves user-provided notes under .gauntlet/annotations/ in the current project.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
