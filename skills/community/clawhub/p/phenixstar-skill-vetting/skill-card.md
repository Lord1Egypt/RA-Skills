## Description: <br>
Vet ClawHub skills for security and utility before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phenixstar](https://clawhub.ai/user/phenixstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate ClawHub skills before installation by combining a lightweight local security scan with manual utility and behavior review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner is heuristic and may miss issues or report false positives, including on example security patterns. <br>
Mitigation: Use scanner output as a review prompt, then manually inspect the skill description, scripts, network behavior, and file operations before installation. <br>
Risk: The skill inspects files in directories selected by the user, which may include sensitive local content. <br>
Mitigation: Run reviews on isolated copies in temporary directories and avoid pointing the scanner at unrelated workspaces or credential stores. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/phenixstar/phenixstar-skill-vetting) <br>
- [Publisher Profile](https://clawhub.ai/user/phenixstar) <br>
- [Project Homepage](https://github.com/PhenixStar/openclaw-skills-collection) <br>
- [Malicious Code Patterns Database](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with terminal commands and scanner findings; JSON is available from the scanner when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local scanner reports file and line references for potential findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata; artifact _meta.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
