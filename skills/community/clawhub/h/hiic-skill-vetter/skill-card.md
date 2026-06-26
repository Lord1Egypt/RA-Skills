## Description: <br>
Practical skill vetting workflow for AI agents. Prioritizes clear yes/no risk judgments, concise conclusions, and business-aware risk tolerance before installing a skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waytobetter619](https://clawhub.ai/user/waytobetter619) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and reviewers use this skill to perform quick first-pass safety reviews of agent skills before installation or portfolio-wide screening. It produces concise yes/no risk judgments, an overall risk level, and an installation verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an advisory triage helper and may miss issues that require deeper review. <br>
Mitigation: Use it for quick first-pass screening and perform stricter manual review for skills that handle credentials, account mutations, publishing, or other high-impact actions. <br>
Risk: The bundled scanner reads files in the target directory to look for risk patterns. <br>
Mitigation: Run the scanner only on the specific skill directory intended for evaluation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands, JSON] <br>
**Output Format:** [Concise text or Markdown risk report with optional scanner JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes yes/no risk flags, risk level, installation verdict, and short notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
