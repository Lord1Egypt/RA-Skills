## Description: <br>
Compare two text files or strings side-by-side or unified. Highlights additions, deletions, and changes with color. Supports word-level diff, ignore-whitespace, and JSON/YAML structural diff modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, reviewers, and operators use this skill to compare files, inline strings, code snippets, and JSON or YAML configuration changes in local workflows and CI checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compared file contents may be printed to the terminal or captured in logs. <br>
Mitigation: Use the skill on appropriate local inputs and avoid sending sensitive comparison output to shared logs. <br>
Risk: YAML structural diff requires PyYAML, which is an optional dependency. <br>
Mitigation: Install PyYAML only from a trusted package source when YAML diff support is needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text or JSON report, with optional colorized diff output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs diff statistics and exits with 0 for identical inputs, 1 for differences, and 2 for errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
