## Description: <br>
Guides agents through a design-before-implementation workflow that explores user intent, compares approaches, writes a reviewed spec, and then hands off to implementation planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill before creative or implementation work to clarify intent, constraints, success criteria, design options, and an approved written spec. It is especially suited to projects where implementation should wait until a design has been reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional browser companion can run a localhost server that stores mockups and records browser selections. <br>
Mitigation: Keep the companion bound to localhost when possible, avoid binding to 0.0.0.0 on untrusted networks, and stop the server when the session is finished. <br>
Risk: The workflow may create and commit design spec files and may persist companion artifacts in the project directory. <br>
Mitigation: Review generated specs and git changes before relying on them, and add .superpowers/ to .gitignore when companion artifacts should not be committed. <br>
Risk: Design proposals may be incomplete, ambiguous, or poorly matched to the user's actual goals. <br>
Mitigation: Use the built-in clarification, user approval, and spec self-review steps before moving to implementation planning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dizhu/idea-to-design) <br>
- [Visual Companion Guide](visual-companion.md) <br>
- [Spec Document Reviewer Prompt Template](spec-document-reviewer-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown prose, design documents, and optional browser mockups with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and commit spec files under docs/superpowers/specs and optionally persist mockups under .superpowers/brainstorm.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
